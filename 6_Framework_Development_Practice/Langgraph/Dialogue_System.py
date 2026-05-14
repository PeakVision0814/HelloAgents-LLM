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
