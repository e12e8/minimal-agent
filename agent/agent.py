# agent.py
# Agent = 控制器，负责调度 Planner / Decision / Tools / State，组织整体执行流程

from agent.planner import plan
from agent.decision import choose_tool
from agent.tools import general_tool, tech_tool
from agent.state import State

# 将工具名称映射到实际函数实现
TOOL_MAP = {
    "general": general_tool,
    "tech": tech_tool,
}


def run_agent(task: str) -> str:
    """
    运行一个简单的 Agent 流程：规划 -> 决策 -> 执行 -> 保存状态 -> 汇总输出。

    参数:
        task (str): 用户的任务描述

    返回:
        str: 汇总后的文本输出（将每步工具返回的 content 拼接）
    """
    # 打印收到的任务，便于调试和观察执行流程
    print(f"\nAgent 接收到任务：{task}")

    # 初始化状态容器并生成执行步骤
    state = State()
    steps = plan(task)

    final_output = ""

    # 依次执行每一步：决策选工具 -> 调用工具 -> 保存结果 -> 汇总
    for step in steps:
        print(f"\n[Step] {step}")

        # 1. 决策层：根据步骤决定使用哪个工具
        tool_name = choose_tool(step)
        tool_func = TOOL_MAP[tool_name]

        print(f"→ 决定使用工具：{tool_name}")

        # 2. 执行工具（实际调用对应函数）
        result = tool_func(step)

        # 3. 保存当前步骤的执行结果到状态容器中
        state.save(step, result)

        # 4. 将工具返回的文本内容追加到最终输出
        final_output += result["content"] + "\n"

    # 返回汇总结果，调用者可进一步格式化或展示
    return final_output
