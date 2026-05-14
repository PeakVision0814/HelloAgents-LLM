from typing import List, TypedDict

from langgraph.graph import END, StateGraph


# 定义全局状态的数据结构
class AgentState(TypedDict):
    messages: List[str]      # 对话历史
    current_task: str        # 当前任务
    final_answer: str        # 最终答案
    # ... 任何其他需要追踪的状态


# 定义一个“规划者”节点函数
def planner_node(state: AgentState) -> AgentState:
    """根据当前任务制定计划，并更新状态。"""
    current_task = state["current_task"]
    # 这里可以替换为真实的 LLM 调用，用来生成计划
    plan = f"为任务 '{current_task}' 生成的计划..."

    # 将新消息追加到状态中
    state["messages"].append(plan)
    return state


# 定义一个“执行者”节点函数
def executor_node(state: AgentState) -> AgentState:
    """执行最新计划，并更新状态。"""
    latest_plan = state["messages"][-1]
    # 这里可以替换为真实的工具调用或 LLM 执行逻辑
    result = f"执行计划 '{latest_plan}' 的结果..."

    state["messages"].append(result)
    return state


def should_continue(state: AgentState) -> str:
    """条件函数：根据状态决定下一步路由。"""
    # 假设如果消息少于 3 条，则需要继续规划
    if len(state["messages"]) < 3:
        # 返回值需要与条件边中定义的键保持一致
        return "continue_to_planner"

    state["final_answer"] = state["messages"][-1]
    return "end_workflow"


# 初始化一个状态图，并绑定我们定义的状态结构
workflow = StateGraph(AgentState)

# 将节点函数添加到图中
workflow.add_node("planner", planner_node)
workflow.add_node("executor", executor_node)

# 设置图的入口点
workflow.set_entry_point("planner")

# 添加常规边，连接 planner 和 executor
workflow.add_edge("planner", "executor")

# 添加条件边，实现动态路由
workflow.add_conditional_edges(
    # 起始节点
    "executor",
    # 判断函数
    should_continue,
    # 路由映射：将判断函数的返回值映射到目标节点
    {
        "continue_to_planner": "planner",  # 继续回到 planner 节点
        "end_workflow": END,               # 结束整个工作流
    },
)

# 编译图，生成可执行的应用
app = workflow.compile()


# 运行图
if __name__ == "__main__":
    inputs: AgentState = {
        "current_task": "分析最近的 AI 行业新闻",
        "messages": [],
        "final_answer": "",
    }

    for event in app.stream(inputs):
        print(event)
