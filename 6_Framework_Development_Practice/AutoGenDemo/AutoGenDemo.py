"""
AutoGen 软件开发团队协作案例
"""

import asyncio
import sys
from pathlib import Path

from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console

CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from llm_clients import create_autogen_openai_client
from roles.registry import DEFAULT_ROLE_SEQUENCE, build_participants

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except AttributeError:
    pass


def create_openai_model_client():
    """创建并配置 OpenAI 模型客户端。"""
    return create_autogen_openai_client()


async def run_software_development_team(role_sequence=None):
    """运行软件开发团队协作。"""
    print("[初始化] 正在初始化模型客户端...")
    model_client = create_openai_model_client()

    print("[初始化] 正在创建智能体团队...")
    participants = build_participants(model_client, role_sequence=role_sequence)

    termination = TextMentionTermination("TERMINATE")

    team_chat = RoundRobinGroupChat(
        participants=participants,
        termination_condition=termination,
        max_turns=20,
    )

    task = """我们需要开发一个比特币价格显示应用，具体要求如下：

核心功能：
- 实时显示比特币当前价格（USD）
- 显示24小时价格变化趋势（涨跌幅和涨跌额）
- 提供价格刷新功能

技术要求：
- 使用 Streamlit 框架创建 Web 应用
- 界面简洁美观，用户友好
- 添加适当的错误处理和加载状态

请团队协作完成这个任务，从需求分析到最终实现。"""

    print("[运行] 启动 AutoGen 软件开发团队协作...")
    print("=" * 60)

    result = await Console(team_chat.run_stream(task=task))

    print("\n" + "=" * 60)
    print("[完成] 团队协作完成！")

    return result


if __name__ == "__main__":
    try:
        # 调整这个序列即可快速增减角色：
        # 1. 新角色文件放到 roles/ 下
        # 2. 在 roles/registry.py 注册
        # 3. 在这里调整顺序或注释掉某个角色键
        role_sequence = DEFAULT_ROLE_SEQUENCE

        result = asyncio.run(run_software_development_team(role_sequence=role_sequence))

        print("\n[结果] 协作结果摘要：")
        print(f"- 参与智能体数量：{len(role_sequence)}个")
        print(f"- 任务完成状态：{'成功' if result else '需要进一步处理'}")

    except ValueError as e:
        print(f"[配置错误] {e}")
        print("请检查 .env 文件中的配置是否正确")
    except Exception as e:
        print(f"[运行错误] {e}")
        import traceback

        traceback.print_exc()
