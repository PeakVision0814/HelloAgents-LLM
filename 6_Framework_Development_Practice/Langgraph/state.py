from typing import Annotated, TypedDict

from langgraph.graph.message import add_messages


class SearchState(TypedDict):
    messages: Annotated[list, add_messages]
    user_query: str      # 用户原始问题
    search_query: str    # 优化后用于 Tavily API 的搜索查询
    search_results: str  # Tavily 搜索返回的精简结果
    final_answer: str    # 最终生成的答案
    step: str            # 标记当前步骤
    retry_count: int     # 搜索重试计数器，防止循环失控
