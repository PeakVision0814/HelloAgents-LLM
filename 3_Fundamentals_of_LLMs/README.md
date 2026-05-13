# Chapter 3: Fundamentals of LLMs

理解大语言模型的本地运行方式——从加载模型到构造 Chat Template 输入。

## Files

| File | Description |
|------|-------------|
| `ch3_local_model.py` | 通过 ModelScope 加载 `Qwen1.5-0.5B-Chat`，使用 chat template 生成回复 |

## Quick Start

```bash
# 安装依赖（首次运行需下载模型，耗时较长）
pip install torch modelscope

# 运行
python ch3_local_model.py
```

GPU 可用时自动使用 CUDA，否则回退 CPU。

## Key Concepts

- **Model Loading**: 从 ModelScope 加载预训练模型和 tokenizer
- **Chat Template**: `tokenizer.apply_chat_template()` 将消息列表转换为模型输入格式
- **Tokenization & Decoding**: 文本 → token IDs → 模型推理 → token IDs → 文本
