# Configure APIs in the local or repo-root .env before running this demo.
from pathlib import Path

from hello_agents import HelloAgentsLLM, SimpleAgent, ToolRegistry
from hello_agents.memory import MemoryConfig
from hello_agents.tools import MemoryTool, RAGTool

CHAPTER_DIR = Path(__file__).resolve().parent
MEMORY_DATA_DIR = CHAPTER_DIR / "memory_data"
KNOWLEDGE_BASE_DIR = CHAPTER_DIR / "knowledge_base"

# Create the LLM client.
llm = HelloAgentsLLM()

# Create the demo agent.
agent = SimpleAgent(
    name="智能助手",
    llm=llm,
    system_prompt="你是一个有记忆和知识检索能力的 AI 助手",
)

# Register tools.
tool_registry = ToolRegistry()

# Memory data is fixed under the Chapter 8 directory.
memory_config = MemoryConfig(storage_path=str(MEMORY_DATA_DIR))
memory_tool = MemoryTool(user_id="user123", memory_config=memory_config)
tool_registry.register_tool(memory_tool)

# RAG temporary files and knowledge-base inputs are also fixed under Chapter 8.
rag_tool = RAGTool(knowledge_base_path=str(KNOWLEDGE_BASE_DIR))
tool_registry.register_tool(rag_tool)

agent.tool_registry = tool_registry

response = agent.run("你好，请记住我叫黄老板，我是一名 Python 开发者")
print(response)
