# Chapter 3: Fundamentals of LLMs

从 tokenization 到 Transformer，逐层理解大语言模型的核心组件。

## Files

| File | Topic | Description |
|------|-------|-------------|
| `N_gram.py` | 统计语言模型 | N-gram 概率计算，理解马尔可夫假设与序列概率建模 |
| `BPE.py` | 分词算法 | Byte Pair Encoding 实现：统计词元对频率，迭代合并 |
| `Word_Embedding.py` | 词向量 | 向量空间中的语义关系演示（king - man + woman ≈ queen） |
| `Transformer.py` | 模型架构 | 从零实现 Multi-Head Attention 及 Transformer Block |
| `Call LLM.py` | 模型调用 | 通过 ModelScope 加载 `Qwen1.5-0.5B-Chat`，Chat Template 推理 |

建议按上表顺序阅读，从数据预处理到模型架构再到推理调用，形成完整认知链路。

## Quick Start

```bash
# BPE、N-gram、Word Embedding 仅需标准库
python N_gram.py
python BPE.py
python Word_Embedding.py

# Transformer 需要 torch
pip install torch
python Transformer.py

# Call LLM 需要下载模型
pip install torch modelscope
python "Call LLM.py"
```

## Key Concepts

- **N-gram**: P(w₃ | w₁,w₂)，用前 n-1 个词预测下一个词
- **BPE**: 从字符级开始，反复合并高频相邻符号对，构建子词词表
- **Word Embedding**: 将离散词映射到稠密向量，捕获语义关系
- **Self-Attention**: Q·Kᵀ 计算 token 间关联权重，是 Transformer 的核心
- **Chat Template**: 将对话消息列表转换为模型可接受的输入格式
