from state import SearchState


def route_after_quality_check(state: SearchState) -> str:
    """根据质量检查结果决定下一跳。"""
    if state["step"] == "quality_retry":
        return "retry_search"
    return "finish"
