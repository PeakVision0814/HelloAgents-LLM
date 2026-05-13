# Hello Agents

从 ELIZA 到 ReAct —— AI Agent 经典范式的 Python 教学实现。

本项目源自 [Datawhale Hello-Agents](https://github.com/datawhalechina/hello-agents) 开源教程，按章节组织，逐步展示智能体从规则系统到 LLM 驱动的演进过程。

## 章节概览

| 章节 | 目录 | 核心内容 | 外部依赖 |
|------|------|----------|----------|
| 1 | [Introduction to Agents](1_Introduction_to_Agents/) | 旅行助手 Agent，Thought-Action-Observation 循环 | LLM API + Tavily |
| 2 | [History of Agents](2_History_of_Agents/) | ELIZA 规则式对话系统 | 无 |
| 3 | [Fundamentals of LLMs](3_Fundamentals_of_LLMs/) | 本地加载 Qwen，Chat Template 调用 | 需下载模型 |
| 4 | [Agent Classical Paradigms](4_Agent_Classical_Paradigm_Construction/) | ReAct / Plan-and-Solve / Reflection | LLM API + SerpApi |
| 5 | [Low-Code Platforms](5_Building_Agents_with_Low_Code_Platforms/) | Dify 工作流 + n8n 自动化 | Dify / n8n 账号 |

此外根目录下的 `tokenizer.py` 演示 BPE 分词算法，独立于章节，无外部依赖。

## 快速开始

```bash
# Python 3.10+
python -m venv .venv
.venv\Scripts\activate

# 按需安装（ELIZA 和 tokenizer 无需任何安装）
pip install openai python-dotenv requests tavily-python google-search-results torch modelscope
```

需要 LLM API 的章节，在对应目录下创建 `.env`：

```env
LLM_MODEL_ID=your-model-id
LLM_API_KEY=your-api-key
LLM_BASE_URL=https://your-api-endpoint
LLM_TIMEOUT=60
SERPAPI_API_KEY=your-serpapi-key
TAVILY_API_KEY=your-tavily-key
```

## 学习路线

推荐由浅入深，先无外部依赖后有外部依赖：

1. [ELIZA](2_History_of_Agents/) —— 规则式对话，零依赖，理解最早的 Agent 形态
2. `tokenizer.py` —— BPE 分词原理，理解 LLM 如何处理文本
3. [本地 LLM](3_Fundamentals_of_LLMs/) —— 下载开源模型，体验 Chat Template 调用
4. [旅行助手](1_Introduction_to_Agents/) —— 第一个 LLM 驱动的 Agent，学会 Thought-Action 循环
5. [ReAct](4_Agent_Classical_Paradigm_Construction/) —— 推理 + 行动闭环，工具调用的标准范式
6. [Plan-and-Solve](4_Agent_Classical_Paradigm_Construction/) —— 先拆解计划，再逐步执行
7. [Reflection](4_Agent_Classical_Paradigm_Construction/) —— 自我审查 + 迭代优化
8. [低代码平台](5_Building_Agents_with_Low_Code_Platforms/) —— Dify / n8n 无需手写循环

> 第 1 章虽然编号靠前，但需要配置 LLM API 和 Tavily 双重密钥，建议按此顺序先跑通无依赖的章节。

## 注意事项

- 示例代码偏教学用途，生产环境需补充错误处理、密钥管理和测试。
- 在线 LLM 调用会产生 API 费用，运行前请确认配置。
- 运行第 4 章时需先 `cd` 进入对应目录，保证模块导入路径正确。
- `.env` 请勿提交到版本库。

## 致谢

本项目为个人学习练习仓库，代码与内容源自 [Datawhale Hello-Agents](https://github.com/datawhalechina/hello-agents) 开源教程，感谢 Datawhale 社区。
