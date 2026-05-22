from dotenv import load_dotenv

from hello_agents import SimpleAgent
from my_gemini_llm import MyGeminiLLM


# 加载根目录 .env
load_dotenv()


def test_gemini_configuration():
    """测试 Gemini 配置是否被正确识别。"""
    print("=== 测试1：Gemini 配置检查 ===")

    llm = MyGeminiLLM()

    print(f"provider: {llm.provider}")
    print(f"model: {llm.model}")
    print(f"base_url: {llm.base_url}")
    print(f"timeout: {llm.timeout}\n")


def test_gemini_direct_call():
    """测试直接调用 MyGeminiLLM。"""
    print("=== 测试2：直接调用 Gemini LLM ===")

    llm = MyGeminiLLM()
    messages = [
        {"role": "system", "content": "你是一个简洁的教学助手。"},
        {"role": "user", "content": "请用三句话介绍什么是 AI Agent。"},
    ]

    print("流式响应: ", end="")
    for chunk in llm.think(messages):
        print(chunk, end="", flush=True)
    print("\n")


def test_gemini_with_simple_agent():
    """测试 Gemini 与 SimpleAgent 的集成。"""
    print("=== 测试3：Gemini + SimpleAgent 集成 ===")

    llm = MyGeminiLLM()
    agent = SimpleAgent(
        name="Gemini助手",
        llm=llm,
        system_prompt="你是一个中文教学助手，回答要直接、清晰。",
    )

    response = agent.run("请解释 ReAct Agent 和普通问答模型的区别。")
    print(f"Agent 响应: {response}\n")


if __name__ == "__main__":
    test_gemini_configuration()
    test_gemini_direct_call()
    test_gemini_with_simple_agent()
