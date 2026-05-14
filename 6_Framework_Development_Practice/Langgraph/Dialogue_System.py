import asyncio
import os
from datetime import datetime
from typing import Annotated, TypedDict

from dotenv import load_dotenv
from langchain_core.messages import AIMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from tavily import TavilyClient


# 加载 .env 文件中的环境变量
load_dotenv()


class SearchState(TypedDict):
    messages: Annotated[list, add_messages]
    user_query: str      # 用户原始问题
    search_query: str    # 优化后用于 Tavily API 的搜索查询
    search_results: str  # Tavily 搜索返回的精简结果
    final_answer: str    # 最终生成的答案
    step: str            # 标记当前步骤
    retry_count: int     # 搜索重试计数器，防止循环失控


# 初始化模型和 Tavily 客户端
llm = ChatOpenAI(
    model=os.getenv("LLM_MODEL_ID", "gpt-4o-mini"),
    api_key=os.getenv("LLM_API_KEY"),
    base_url=os.getenv("LLM_BASE_URL", "https://api.openai.com/v1"),
    temperature=0.7,
)

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
TODAY_STR = datetime.now().strftime("%Y-%m-%d")


def truncate_text(text: str, max_length: int = 300) -> str:
    """截断过长文本，避免提示词超长。"""
    clean_text = " ".join(text.split())
    if len(clean_text) <= max_length:
        return clean_text
    return clean_text[:max_length] + "..."


async def stream_llm_response(prompt: str) -> str:
    """以流式方式获取模型输出，并实时打印到终端。"""
    chunks = []
    async for chunk in llm.astream(prompt):
        text = chunk.content if isinstance(chunk.content, str) else str(chunk.content)
        if not text:
            continue
        print(text, end="", flush=True)
        chunks.append(text)

    print()
    return "".join(chunks)


async def understand_and_query_node(state: SearchState) -> dict:
    """理解用户意图，并生成更适合搜索引擎的查询语句。"""
    prompt = f"""
你是一个搜索查询优化助手。
今天的日期是：{TODAY_STR}

请根据用户问题完成两件事：
1. 理解用户真正想问的核心意图。
2. 生成一个更适合搜索引擎检索的精炼搜索关键词或搜索短句。

请严格遵守以下规则：
- 如果用户问“最近”“最新”“当前”“今年”等时效性问题，必须保留当前时间语境。
- 不要把时间错误改写成 2023、2024 等过去年份，除非用户明确指定那个年份。
- 如果用户没有明确给出年份，但问题明显是在问当下，请优先使用 2026 年或 {TODAY_STR} 附近的时间表达。

用户问题：
{state["user_query"]}

请严格按照下面格式输出：
Intent: <用户问题的核心意图>
Search Query: <适合搜索的关键词或短句>
""".strip()

    response = await llm.ainvoke(prompt)
    content = response.content if isinstance(response.content, str) else str(response.content)

    intent = ""
    search_query = state["user_query"]

    for line in content.splitlines():
        if line.startswith("Intent:"):
            intent = line.replace("Intent:", "", 1).strip()
        elif line.startswith("Search Query:"):
            search_query = line.replace("Search Query:", "", 1).strip()

    if any(keyword in state["user_query"] for keyword in ["最近", "最新", "当前", "今年"]):
        if "2026" not in search_query and TODAY_STR[:4] not in search_query:
            search_query = f"{TODAY_STR[:4]}年 {search_query}"

    return {
        "search_query": search_query,
        "step": "understand_and_query",
        "messages": [
            AIMessage(content=f"意图理解：{intent}\n搜索查询：{search_query}")
        ],
    }


async def search_node(state: SearchState) -> dict:
    """调用 Tavily API 执行真实搜索，并处理可能出现的异常。"""
    next_retry_count = state["retry_count"] + 1

    try:
        response = await asyncio.to_thread(
            tavily_client.search,
            query=state["search_query"],
            search_depth="basic",
            max_results=3,
            include_answer=True,
        )

        result_lines = []

        if response.get("answer"):
            result_lines.append(f"总结：{truncate_text(response['answer'], 400)}")

        for index, item in enumerate(response.get("results", []), start=1):
            title = truncate_text(item.get("title", "无标题"), 120)
            content = truncate_text(item.get("content", "无内容"), 220)
            url = item.get("url", "无链接")
            result_lines.append(
                f"{index}. 标题：{title}\n内容：{content}\n链接：{url}"
            )

        search_results = "\n\n".join(result_lines) if result_lines else "没有检索到有价值的结果。"

        return {
            "search_results": search_results,
            "step": "search_completed",
            "retry_count": next_retry_count,
            "messages": [
                AIMessage(
                    content=(
                        f"搜索完成，第 {next_retry_count} 次检索。\n"
                        f"使用查询：{state['search_query']}"
                    )
                )
            ],
        }
    except Exception as error:
        return {
            "search_results": f"搜索失败：{error}",
            "step": "search_failed",
            "retry_count": next_retry_count,
            "messages": [
                AIMessage(
                    content=(
                        f"搜索阶段失败，第 {next_retry_count} 次检索。\n"
                        f"错误信息：{error}"
                    )
                )
            ],
        }


async def answer_node(state: SearchState) -> dict:
    """根据搜索是否成功，选择不同策略生成最终回答。"""
    if state["step"] == "search_failed":
        prompt = f"""
你是一个有帮助的问答助手。
今天的日期是：{TODAY_STR}

用户的问题是：
{state["user_query"]}

搜索阶段失败了，无法获取实时互联网信息。
请基于你已有的知识尽力回答这个问题，同时明确告诉用户：
1. 这次回答没有使用到实时搜索结果。
2. 回答可能不包含最新信息。
3. 如果用户需要，我可以稍后再次尝试搜索。
""".strip()
    else:
        prompt = f"""
你是一个有帮助的问答助手。
今天的日期是：{TODAY_STR}

请根据用户问题和搜索结果，生成一个清晰、准确、有条理的回答。

用户问题：
{state["user_query"]}

搜索结果：
{truncate_text(state["search_results"], 1800)}

请在回答中尽量体现这些搜索结果提供的实时信息，并保持语言自然易懂。
""".strip()

    print("💡 最终回答")
    final_answer = await stream_llm_response(prompt)

    return {
        "final_answer": final_answer,
        "step": "answer_completed",
        "messages": [
            AIMessage(content=f"最终回答：{final_answer}")
        ],
    }


async def quality_check_node(state: SearchState) -> dict:
    """检查答案质量，决定是否需要再次搜索。"""
    if state["retry_count"] > 2:
        return {
            "step": "quality_pass",
            "messages": [
                AIMessage(content="质量检查：已超过 2 次重试，强制通过。")
            ],
        }

    prompt = f"""
你是一个答案质量检查员。
今天的日期是：{TODAY_STR}

请检查下面这个回答是否足够满足用户问题。

用户问题：
{state["user_query"]}

搜索查询：
{state["search_query"]}

搜索结果摘要：
{truncate_text(state["search_results"], 1200)}

当前回答：
{truncate_text(state["final_answer"], 1200)}

请重点检查：
1. 回答是否真正回应了用户问题。
2. 回答是否足够清晰、具体。
3. 如果回答明显空泛、偏题、信息不足，应该要求重新搜索。

请严格只输出一个词：
PASS
或
RETRY
""".strip()

    response = await llm.ainvoke(prompt)
    decision = response.content if isinstance(response.content, str) else str(response.content)
    decision = decision.strip().upper()

    if "RETRY" in decision:
        return {
            "step": "quality_retry",
            "messages": [
                AIMessage(content="质量检查：当前答案信息不足，准备重新搜索。")
            ],
        }

    return {
        "step": "quality_pass",
        "messages": [
            AIMessage(content="质量检查：当前答案质量通过。")
        ],
    }


def route_after_quality_check(state: SearchState) -> str:
    """根据质量检查结果决定下一跳。"""
    if state["step"] == "quality_retry":
        return "retry_search"
    return "finish"


# 构建状态图
workflow = StateGraph(SearchState)

# 添加节点
workflow.add_node("understand_and_query", understand_and_query_node)
workflow.add_node("search", search_node)
workflow.add_node("answer", answer_node)
workflow.add_node("quality_check", quality_check_node)

# 添加边
workflow.add_edge(START, "understand_and_query")
workflow.add_edge("understand_and_query", "search")
workflow.add_edge("search", "answer")
workflow.add_edge("answer", "quality_check")
workflow.add_conditional_edges(
    "quality_check",
    route_after_quality_check,
    {
        "retry_search": "search",
        "finish": END,
    },
)

# 编译图，生成可执行应用
app = workflow.compile()


async def run_single_query(user_query: str) -> None:
    """异步运行一次完整问答流程。"""
    inputs: SearchState = {
        "messages": [],
        "user_query": user_query,
        "search_query": "",
        "search_results": "",
        "final_answer": "",
        "step": "",
        "retry_count": 0,
    }

    print("开始运行三步问答助手...\n")

    async for event in app.astream(inputs):
        if "understand_and_query" in event:
            node_state = event["understand_and_query"]
            print("🧠 理解阶段")
            print(f"原始问题：{user_query}")
            print(f"优化查询：{node_state['search_query']}\n")
        elif "search" in event:
            node_state = event["search"]
            print("🔍 搜索阶段")
            print(f"搜索状态：{node_state['step']}")
            print(f"当前重试次数：{node_state['retry_count']}")
            print(f"搜索结果摘要：\n{node_state['search_results']}\n")
        elif "answer" in event:
            print()
        elif "quality_check" in event:
            node_state = event["quality_check"]
            print("🔁 质量检查")
            print(f"检查结果：{node_state['step']}\n")


async def main() -> None:
    """循环提问入口。"""
    print("进入三步问答助手，输入 exit 或 quit 结束。\n")

    while True:
        user_query = input("🤔 您想了解什么：").strip()

        if not user_query:
            print("问题不能为空，请重新输入。\n")
            continue

        if user_query.lower() in {"exit", "quit"}:
            print("已退出三步问答助手。")
            break

        await run_single_query(user_query)
        print("-" * 60)


if __name__ == "__main__":
    asyncio.run(main())
