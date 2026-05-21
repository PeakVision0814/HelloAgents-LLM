from langgraph.graph import END, START, StateGraph
import asyncio

from edges import route_after_quality_check
from nodes import (
    answer_node,
    quality_check_node,
    search_node,
    understand_and_query_node,
)
from state import SearchState


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
