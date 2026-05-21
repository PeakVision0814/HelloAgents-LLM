"""用户代理角色定义。"""

from autogen_agentchat.agents import UserProxyAgent


async def auto_user_input(prompt: str, cancellation_token=None) -> str:
    """脚本模式下自动结束对话，避免阻塞等待人工输入。"""
    return "测试完成，TERMINATE"


def create_user_proxy():
    """创建非交互式用户代理智能体。"""
    return UserProxyAgent(
        name="UserProxy",
        description="用户代理，负责代表最终用户完成简单验收，并在脚本模式下自动结束对话。",
        input_func=auto_user_input,
    )
