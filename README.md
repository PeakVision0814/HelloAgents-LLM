# Agent Study

这是一个用于学习和实践 AI Agent 基础概念的 Python 示例项目。项目按章节组织，从早期规则式对话系统、LLM 基础调用，到 ReAct、Plan-and-Solve、Reflection 等经典 Agent 构造范式，逐步展示智能体的核心组成方式。

## 项目结构

```text
agent_study/
├── tokenizer.py
├── 1_Introduction_to_Agents/
│   └── travel_agent.py
├── 2_History_of_Agents/
│   └── ELIZA.py
├── 3_Fundamentals_of_LLMs/
│   └── ch3_local_model.py
├── 4_Agent_Classical_Paradigm_Construction/
│   ├── llm_client.py
│   ├── tools.py
│   ├── ReAct.py
│   ├── Plan_and_solve.py
│   └── Reflection.py
└── 5_Building_Agents_with_Low_Code_Platforms/
    ├── Chatflow-AI_news-draft-9211.zip
    ├── HelloAgent_n8nCase.json
    └── 超级智能个人助手.yml
```

## 示例说明

### `tokenizer.py`

演示 BPE(Byte Pair Encoding) 分词算法的核心思想：统计相邻词元对的频次，并反复合并出现频率最高的词元对。适合理解大语言模型 tokenizer 的基本训练过程。

运行方式：

```bash
python tokenizer.py
```

### `1_Introduction_to_Agents/travel_agent.py`

一个旅行助手 Agent 示例。它通过大语言模型输出 `Thought` 和 `Action`，并调用天气查询与景点搜索工具完成任务。

主要能力：

- 使用 `wttr.in` 查询指定城市天气。
- 使用 Tavily Search 根据城市和天气推荐景点。
- 使用兼容 OpenAI API 的模型服务驱动 Agent 推理。

运行前需要配置或替换：

- LLM API Key、Base URL、模型 ID。
- `TAVILY_API_KEY`。

建议将密钥放入环境变量或 `.env` 文件中，避免把真实密钥提交到仓库。

运行方式：

```bash
python 1_Introduction_to_Agents/travel_agent.py
```

### `2_History_of_Agents/ELIZA.py`

一个简化版 ELIZA 对话程序，用正则规则和模板回复模拟早期聊天机器人。

主要能力：

- 根据输入匹配预设正则规则。
- 对第一人称和第二人称代词进行简单转换。
- 在命令行中进行循环对话。

运行方式：

```bash
python 2_History_of_Agents/ELIZA.py
```

输入 `quit`、`exit` 或 `bye` 结束对话。

### `3_Fundamentals_of_LLMs/ch3_local_model.py`

演示通过 ModelScope 加载本地开源模型 `Qwen/Qwen1.5-0.5B-Chat`，并使用 chat template 构造输入、调用模型生成回复。

主要依赖：

- `torch`
- `modelscope`

运行方式：

```bash
python 3_Fundamentals_of_LLMs/ch3_local_model.py
```

如果本机支持 CUDA，脚本会优先使用 GPU；否则使用 CPU。

### `4_Agent_Classical_Paradigm_Construction/llm_client.py`

封装兼容 OpenAI Chat Completions API 的 LLM 客户端 `HelloAgentsLLM`。它会从 `.env` 或系统环境变量中读取配置，并默认使用流式响应。

需要的环境变量：

```env
LLM_MODEL_ID=your-model-id
LLM_API_KEY=your-api-key
LLM_BASE_URL=https://your-compatible-api-endpoint
LLM_TIMEOUT=60
```

### `4_Agent_Classical_Paradigm_Construction/tools.py`

定义工具执行器 `ToolExecutor` 以及两个可供 Agent 调用的工具：

- **`calculate`** — 安全数学计算器，支持 `+ - * / ** % //` 及常用数学函数（`sqrt`, `sin`, `cos`, `log` 等），自动将中文符号（× ÷）转为标准运算符。使用受限执行环境（沙箱），无需外部 API Key。
- **`search`** — 基于 SerpApi 的网页搜索引擎，智能解析答案框、知识图谱和有机搜索结果。

需要的环境变量（仅 `search` 工具需要）：

```env
SERPAPI_API_KEY=your-serpapi-key
```

### `4_Agent_Classical_Paradigm_Construction/ReAct.py`

实现 ReAct(Reasoning + Acting) Agent。模型按 `Thought` / `Action` 格式推理，在需要外部信息时调用工具，并把观察结果加入历史继续迭代。

运行方式：

```bash
cd 4_Agent_Classical_Paradigm_Construction
python ReAct.py
```

### `4_Agent_Classical_Paradigm_Construction/Plan_and_solve.py`

实现 Plan-and-Solve 范式：先由 Planner 将复杂问题拆解成步骤，再由 Executor 按步骤执行并得到最终答案。

运行方式：

```bash
cd 4_Agent_Classical_Paradigm_Construction
python Plan_and_solve.py
```

### `4_Agent_Classical_Paradigm_Construction/Reflection.py`

实现 Reflection 范式：Agent 先生成代码，再由反思提示审查算法效率，并根据反馈迭代优化。

运行方式：

```bash
cd 4_Agent_Classical_Paradigm_Construction
python Reflection.py
```

### `5_Building_Agents_with_Low_Code_Platforms/`

使用 Dify 和 n8n 等低代码平台搭建 Agent 工作流，无需手写 Agent Loop。

| 文件 | 平台 | 用途 |
|------|------|------|
| `Chatflow-AI_news-draft-9211.zip` | Dify | AI 新闻稿生成 Chatflow |
| `超级智能个人助手.yml` | Dify | 多功能个人助手 DSL 工作流 |
| `HelloAgent_n8nCase.json` | n8n | Gmail 触发 + AI 自动化工作流 |

使用方式：在对应平台的 Studio 中选择 **Import** 上传文件，配置凭据后即可运行。

## 环境准备

建议使用 Python 3.10 或更高版本，并创建虚拟环境：

```bash
python -m venv .venv
.venv\Scripts\activate
```

项目当前没有提供 `requirements.txt`，可按需要安装示例依赖：

```bash
pip install openai python-dotenv requests tavily-python google-search-results torch modelscope
```

其中：

- 只运行 `ELIZA.py` 或 `tokenizer.py` 时，不需要安装 LLM 相关依赖。
- 运行本地模型示例需要安装 `torch` 和 `modelscope`，并可能需要较长的模型下载时间。
- 运行联网工具示例需要可用的 API Key 和网络环境。

## `.env` 示例

在项目根目录或对应章节目录下创建 `.env` 文件：

```env
LLM_MODEL_ID=qwen-flash
LLM_API_KEY=your-api-key
LLM_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
LLM_TIMEOUT=60

SERPAPI_API_KEY=your-serpapi-key
TAVILY_API_KEY=your-tavily-key
```

请不要将真实 `.env` 文件提交到版本库。

## 学习路线

推荐按下面顺序阅读和运行（由浅入深，先无外部依赖后有外部依赖）：

1. `2_History_of_Agents/ELIZA.py`：理解早期规则式 Agent。纯本地运行，无需任何 API Key 或 GPU。
2. `tokenizer.py`：理解 BPE tokenizer 的基本训练过程。纯本地运行。
3. `3_Fundamentals_of_LLMs/ch3_local_model.py`：理解本地 LLM 的输入构造和生成。需要下载模型但无需 API Key。
4. `1_Introduction_to_Agents/travel_agent.py`：理解工具调用式 Agent 的基本循环。需要配置 LLM API 和 Tavily API Key。
5. `4_Agent_Classical_Paradigm_Construction/ReAct.py`：学习 ReAct 推理与行动闭环。
6. `4_Agent_Classical_Paradigm_Construction/Plan_and_solve.py`：学习计划拆解和逐步执行。
7. `4_Agent_Classical_Paradigm_Construction/Reflection.py`：学习基于反馈的自我改进。
8. `5_Building_Agents_with_Low_Code_Platforms/`：了解如何使用 Dify、n8n 等低代码平台快速搭建 Agent。

> 第1章虽名为"Introduction"，但因涉及 LLM API 和搜索引擎 API 的双重配置，建议在熟悉本地示例后再回头学习。第4章的三个 Agent 共享 `llm_client.py` 和 `tools.py` 作为公共基础设施，阅读时建议先理解这两个模块。

## 注意事项

- 部分 Python 文件包含中文注释和提示词，建议使用 UTF-8 编码打开。
- 在线搜索和 LLM 调用示例会产生 API 调用成本，请确认配置后再运行。
- 示例代码偏教学用途，主要用于展示 Agent 思路；在生产环境使用前需要补充异常处理、密钥管理、日志和测试。
- 若运行 `4_Agent_Classical_Paradigm_Construction` 下的脚本，请先进入该目录，保证本地模块导入路径正确。

## 致谢

本项目是个人学习练习仓库，代码和内容源自 [Datawhale Hello-Agents](https://github.com/datawhalechina/hello-agents) 开源教程。感谢 Datawhale 社区的无私贡献。
