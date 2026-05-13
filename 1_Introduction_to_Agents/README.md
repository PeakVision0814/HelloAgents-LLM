# Chapter 1: Introduction to Agents

从零构建一个由 LLM 驱动的智能旅行助手，理解 Agent 的核心循环：Thought → Action → Observation。

## Files

| File | Description |
|------|-------------|
| `travel_agent.py` | 旅行助手 Agent，调用 `wttr.in` 查天气 + Tavily 搜景点，LLM 驱动推理循环 |
| `FirstAgentTest.ipynb` | Jupyter 交互式笔记，逐步体验 Agent 各组件 |

## Quick Start

```bash
# 安装依赖
pip install openai requests tavily-python

# 配置环境变量
export TAVILY_API_KEY=your-key
export LLM_API_KEY=your-key
export LLM_BASE_URL=https://your-api-endpoint
export LLM_MODEL_ID=your-model

# 运行
python travel_agent.py
```

## Key Concepts

- **Agent Loop**: Thought → Action → Observation 闭环
- **Tool Use**: LLM 自主决定何时调用哪个外部工具
- **Structured Output**: 通过 Prompt 约束模型输出 `Thought:` / `Action:` 格式
