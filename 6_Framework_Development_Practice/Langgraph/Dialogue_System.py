import os
from typing import Annotated, TypedDict

from dotenv import load_dotenv
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI
from tavily import TavilyClient


# 加载 .env 文件中的环境变量
load_dotenv()


class SearchState(TypedDict):
    messages: Annotated[list, add_messages]
    user_query: str      # 用户原始问题
    search_query: str    # 优化后用于 Tavily API 的搜索查询
    search_results: str  # Tavily 搜索返回的结果
    final_answer: str    # 最终生成的答案
    step: str            # 标记当前步骤


# 初始化模型和 Tavily 客户端
llm = ChatOpenAI(
    model=os.getenv("LLM_MODEL_ID", "gpt-4o-mini"),
    api_key=os.getenv("LLM_API_KEY"),
    base_url=os.getenv("LLM_BASE_URL", "https://api.openai.com/v1"),
    temperature=0.7,
)

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


def understand_and_query_node(state: SearchState) -> dict:
    """理解用户意图，并生成更适合搜索引擎的查询语句。"""
    prompt = f"""
你是一个搜索查询优化助手。

请根据用户问题完成两件事：
1. 理解用户真正想问的核心意图。
2. 生成一个更适合搜索引擎检索的精炼搜索关键词或搜索短句。

用户问题：
{state["user_query"]}

请严格按照下面格式输出：
Intent: <用户问题的核心意图>
Search Query: <适合搜索的关键词或短句>
""".strip()

    response = llm.invoke(prompt)
    content = response.content if isinstance(response.content, str) else str(response.content)

    intent = ""
    search_query = state["user_query"]

    for line in content.splitlines():
        if line.startswith("Intent:"):
            intent = line.replace("Intent:", "", 1).strip()
        elif line.startswith("Search Query:"):
            search_query = line.replace("Search Query:", "", 1).strip()

    return {
        "search_query": search_query,
        "step": "understand_and_query",
        "messages": [
            {
                "role": "assistant",
                "content": f"意图理解：{intent}\n搜索查询：{search_query}",
            }
        ],
    }


def search_node(state: SearchState) -> dict:
    """调用 Tavily API 执行真实搜索，并处理可能出现的异常。"""
    try:
        response = tavily_client.search(
            query=state["search_query"],
            search_depth="basic",
            max_results=5,
            include_answer=True,
        )

        search_results = str(response)

        return {
            "search_results": search_results,
            "step": "search_completed",
            "messages": [
                {
                    "role": "assistant",
                    "content": f"搜索完成，已获取搜索结果：{state['search_query']}",
                }
            ],
        }
    except Exception as error:
        return {
            "search_results": f"搜索失败：{error}",
            "step": "search_failed",
            "messages": [
                {
                    "role": "assistant",
                    "content": f"搜索阶段失败：{error}",
                }
            ],
        }


def answer_node(state: SearchState) -> dict:
    """根据搜索是否成功，选择不同策略生成最终回答。"""
    if state["step"] == "search_failed":
        prompt = f"""
你是一个有帮助的问答助手。

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

请根据用户问题和搜索结果，生成一个清晰、准确、有条理的回答。

用户问题：
{state["user_query"]}

搜索结果：
{state["search_results"]}

请在回答中尽量体现这些搜索结果提供的实时信息，并保持语言自然易懂。
""".strip()

    response = llm.invoke(prompt)
    final_answer = response.content if isinstance(response.content, str) else str(response.content)

    return {
        "final_answer": final_answer,
        "step": "answer_completed",
        "messages": [
            {
                "role": "assistant",
                "content": f"最终回答：{final_answer}",
            }
        ],
    }
