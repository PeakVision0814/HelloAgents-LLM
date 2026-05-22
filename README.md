# Hello Agents

从 ELIZA 到 ReAct —— AI Agent 经典范式的 Python 教学实现。

本项目源自 [Datawhale Hello-Agents](https://github.com/datawhalechina/hello-agents) 开源教程，按章节组织，逐步展示智能体从规则系统到 LLM 驱动的演进过程。

## 章节概览

| 章节 | 目录 | 核心内容 | 外部依赖 |
|------|------|----------|----------|
| 1 | [Introduction to Agents](1_Introduction_to_Agents/) | 旅行助手 Agent，Thought-Action-Observation 循环 | LLM API + Tavily |
| 2 | [History of Agents](2_History_of_Agents/) | ELIZA 规则式对话系统 | 无 |
| 3 | [Fundamentals of LLMs](3_Fundamentals_of_LLMs/) | N-gram / BPE / Embedding / Transformer / 本地模型调用 | 部分需 torch + 模型下载 |
| 4 | [Agent Classical Paradigms](4_Agent_Classical_Paradigm_Construction/) | ReAct / Plan-and-Solve / Reflection | LLM API + SerpApi |
| 5 | [Low-Code Platforms](5_Building_Agents_with_Low_Code_Platforms/) | Dify 工作流 + n8n 自动化 | Dify / n8n 账号 |

## 快速开始

```bash
# Python 3.10+
python -m venv .venv
.venv\Scripts\activate

# 全部依赖（ELIZA 无需安装）
pip install -r requirements.txt
```

需要 LLM API 的章节，建议统一在项目根目录创建 `.env`：

```env
LLM_MODEL_ID=your-model-id
LLM_API_KEY=your-api-key
LLM_BASE_URL=https://your-api-endpoint
LLM_TIMEOUT=60
GEMINI_API_KEY=your-gemini-api-key
GEMINI_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
GEMINI_MODEL_ID=gemini-3.5-flash
SERPAPI_API_KEY=your-serpapi-key
TAVILY_API_KEY=your-tavily-key
```

第 1 章现在也会直接从根目录 `.env` 读取 `LLM_MODEL_ID`、`LLM_API_KEY`、`LLM_BASE_URL` 和 `TAVILY_API_KEY`，不再需要把凭据写在源码里。

项目中的 LLM 配置统一由根目录 [llm_clients.py](llm_clients.py) 管理。教学案例需要 OpenAI 兼容客户端、LangChain `ChatOpenAI` 或 AutoGen `OpenAIChatCompletionClient` 时，都应优先复用这个文件里的函数或类。

## 统一 LLM 客户端用法

[llm_clients.py](llm_clients.py) 会自动读取项目根目录 `.env`，并把常用的 LLM 客户端创建方式集中到一处。新增教学案例时，优先复用这里的入口，避免在每个章节里重复写 `load_dotenv()`、`os.getenv()` 和客户端初始化逻辑。

### 普通 OpenAI 兼容接口

适合第 1 章、第 4 章这类直接调用 Chat Completions 的示例。

```python
from llm_clients import HelloAgentsLLM

llm = HelloAgentsLLM()

answer = llm.generate(
    prompt="你好，请介绍一下 AI Agent。",
    system_prompt="你是一个有帮助的教学助手。",
)
print(answer)
```

如果需要流式输出，使用 `think()`：

```python
from llm_clients import HelloAgentsLLM

llm = HelloAgentsLLM()
response = llm.think([
    {"role": "system", "content": "你是一个 Python 教学助手。"},
    {"role": "user", "content": "写一个快速排序算法。"},
])
```

### LangChain / LangGraph

适合第 6 章 LangGraph 示例，返回的是 `langchain_openai.ChatOpenAI` 实例。

```python
from llm_clients import create_chat_openai

llm = create_chat_openai(temperature=0.7)
response = llm.invoke("用一句话解释 ReAct Agent。")
print(response.content)
```

`6_Framework_Development_Practice/Langgraph/Dialogue_System.py` 这个示例现在会在真实搜索前先做一次敏感词检查；命中后会直接拒答并终止流程，未命中才继续搜索。

### AutoGen

适合 AutoGen 示例，返回的是 `autogen_ext.models.openai.OpenAIChatCompletionClient` 实例。

```python
from llm_clients import create_autogen_openai_client

model_client = create_autogen_openai_client()
```

### 在子目录脚本中导入

如果脚本位于章节子目录，直接运行时 Python 可能找不到根目录模块。可以在脚本开头加入项目根目录到 `sys.path`：

```python
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]  # 按脚本所在层级调整 parents
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from llm_clients import HelloAgentsLLM
```

## 学习路线

推荐由浅入深，先无外部依赖后有外部依赖：

1. [ELIZA](2_History_of_Agents/) —— 规则式对话，零依赖，理解最早的 Agent 形态
2. [LLM 基础](3_Fundamentals_of_LLMs/) —— N-gram → BPE → Embedding → Transformer → 本地模型推理，逐层理解 LLM
3. [旅行助手](1_Introduction_to_Agents/) —— 第一个 LLM 驱动的 Agent，学会 Thought-Action 循环
4. [ReAct](4_Agent_Classical_Paradigm_Construction/) —— 推理 + 行动闭环，工具调用的标准范式
5. [Plan-and-Solve](4_Agent_Classical_Paradigm_Construction/) —— 先拆解计划，再逐步执行
6. [Reflection](4_Agent_Classical_Paradigm_Construction/) —— 自我审查 + 迭代优化
7. [低代码平台](5_Building_Agents_with_Low_Code_Platforms/) —— Dify / n8n 无需手写循环

> 第 1 章虽然编号靠前，但需要配置 LLM API 和 Tavily 双重密钥，建议按此顺序先跑通无依赖的章节。

## 注意事项

- 示例代码偏教学用途，生产环境需补充错误处理、密钥管理和测试。
- 在线 LLM 调用会产生 API 费用，运行前请确认配置。
- 运行第 4 章时需先 `cd` 进入对应目录，保证模块导入路径正确。
- `.env` 请勿提交到版本库。

## 致谢

本项目为个人学习练习仓库，代码与内容源自 [Datawhale Hello-Agents](https://github.com/datawhalechina/hello-agents) 开源教程，感谢 Datawhale 社区。
