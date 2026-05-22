#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
代码示例 01: MemoryTool 基础操作
展示 MemoryTool 的核心 execute 方法和基础操作。
"""

from pathlib import Path

from dotenv import load_dotenv

from hello_agents.memory import MemoryConfig
from hello_agents.tools import MemoryTool

load_dotenv()

CHAPTER_DIR = Path(__file__).resolve().parent
MEMORY_DATA_DIR = CHAPTER_DIR / "memory_data"


def memory_tool_execute_demo():
    """MemoryTool execute 方法演示"""
    print("MemoryTool 基础操作演示")
    print("=" * 50)

    memory_config = MemoryConfig(storage_path=str(MEMORY_DATA_DIR))
    memory_tool = MemoryTool(
        user_id="demo_user",
        memory_config=memory_config,
        memory_types=["working", "episodic", "semantic", "perceptual"],
    )

    print("MemoryTool 初始化完成")
    print("支持的操作: add, search, summary, stats, update, remove, forget, consolidate, clear_all")
    return memory_tool


def add_memory_demo(memory_tool):
    """添加记忆演示"""
    print("\n添加记忆演示")
    print("-" * 30)

    result = memory_tool.run({
        "action": "add",
        "content": "正在学习 HelloAgents 框架的记忆系统",
        "memory_type": "working",
        "importance": 0.7,
        "task_type": "learning",
    })
    print(f"工作记忆: {result}")

    result = memory_tool.run({
        "action": "add",
        "content": "2024 年开始深入研究 AI Agent 技术",
        "memory_type": "episodic",
        "importance": 0.8,
        "event_type": "milestone",
        "location": "研发中心",
    })
    print(f"情景记忆: {result}")

    result = memory_tool.run({
        "action": "add",
        "content": "记忆系统包括工作记忆、情景记忆、语义记忆和感知记忆四种类型",
        "memory_type": "semantic",
        "importance": 0.9,
        "concept": "memory_types",
        "domain": "cognitive_science",
    })
    print(f"语义记忆: {result}")

    result = memory_tool.run({
        "action": "add",
        "content": "查看了记忆系统的架构图和实现代码",
        "memory_type": "perceptual",
        "importance": 0.6,
        "modality": "document",
        "source": "technical_documentation",
    })
    print(f"感知记忆: {result}")


def search_memory_demo(memory_tool):
    """搜索记忆演示"""
    print("\n搜索记忆演示")
    print("-" * 30)

    print("基础搜索 - '记忆系统':")
    result = memory_tool.run({"action": "search", "query": "记忆系统", "limit": 3})
    print(result)

    print("\n按类型搜索 - 语义记忆中的 '记忆':")
    result = memory_tool.run({
        "action": "search",
        "query": "记忆",
        "memory_type": "semantic",
        "limit": 2,
    })
    print(result)

    print("\n高重要性记忆搜索:")
    result = memory_tool.run({
        "action": "search",
        "query": "AI Agent",
        "min_importance": 0.7,
        "limit": 3,
    })
    print(result)


def memory_summary_demo(memory_tool):
    """记忆摘要演示"""
    print("\n记忆摘要演示")
    print("-" * 30)

    result = memory_tool.run({"action": "summary", "limit": 5})
    print("记忆摘要:")
    print(result)

    print("\n统计信息:")
    result = memory_tool.run({"action": "stats"})
    print(result)


def memory_management_demo(memory_tool):
    """记忆管理演示"""
    print("\n记忆管理演示")
    print("-" * 30)

    memory_tool.run({
        "action": "add",
        "content": "这是一个临时的测试记忆，重要性很低",
        "memory_type": "working",
        "importance": 0.1,
    })

    print("基于重要性的遗忘 (阈值 0.2):")
    result = memory_tool.run({
        "action": "forget",
        "strategy": "importance_based",
        "threshold": 0.2,
    })
    print(result)

    print("\n记忆整合 (working -> episodic):")
    result = memory_tool.run({
        "action": "consolidate",
        "from_type": "working",
        "to_type": "episodic",
        "importance_threshold": 0.6,
    })
    print(result)


def main():
    """主函数"""
    print("MemoryTool 基础操作完整演示")
    print("展示记忆系统的核心功能和操作方法")
    print("=" * 60)

    try:
        memory_tool = memory_tool_execute_demo()
        add_memory_demo(memory_tool)
        search_memory_demo(memory_tool)
        memory_summary_demo(memory_tool)
        memory_management_demo(memory_tool)

        print("\n" + "=" * 60)

        print("\n演示的核心功能:")
        print("1. 四种记忆类型的添加和管理")
        print("2. 智能语义搜索和过滤")
        print("3. 记忆摘要和统计分析")
        print("4. 记忆整合和选择性遗忘")

        print("\n设计特点:")
        print("- 统一的 execute 接口，操作简洁一致")
        print("- 丰富的元数据支持，便于分类和检索")
        print("- 智能的重要性评估和时间衰减机制")
        print("- 模拟人类认知的记忆管理策略")

    except Exception as e:
        print(f"\n演示过程中发生错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()