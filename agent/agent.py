# agent.py
# =========================================================
# Agent 控制器
# 职责：
# - 组织 Planner / Decision / Tool / State / Reflection
# - 维护 Agent 的主控制循环（Control Loop）
# =========================================================

from agent.planner import plan
from agent.decision import choose_tool
from agent.tools import general_tool, tech_tool
from agent.state import State
from agent.reflection import reflect, ReflectionDecision

# 工具注册表：Agent 只“选择”，不关心工具内部实现
TOOL_MAP = {
    "general": general_tool,
    "tech": tech_tool,
}


def run_agent(task: str) -> str:
    """
    Agent 主入口函数
    本函数体现 Agent 的完整运行机制：
    Planner → Decision → Execution → Reflection → State
    """
    print(f"\nAgent 接收到任务：{task}")

    # ===============================
    # 初始化 Agent 运行上下文
    # ===============================
    state = State()          # Agent 的短期 / 中期记忆
    steps = plan(task)       # Planner：任务拆解
    final_output = ""

    # =====================================================
    # Agent Control Loop（核心控制循环）
    # 每一个 step 都是一轮完整的 Agent 决策-执行-反思
    # =====================================================
    for step in steps:
        print(f"\n[Step] {step}")

        # -------------------------------------------------
        # 【Decision Layer｜决策层】
        # - 只读取信息（step / state）
        # - 不执行工具
        # - 只产出“使用哪个能力”的决策
        # -------------------------------------------------
        tool_name = choose_tool(step, state)
        tool_func = TOOL_MAP[tool_name]

        print(f"→ 决策：选择工具 {tool_name}")

        # -------------------------------------------------
        # 【Execution Layer｜执行层】
        # - 被动执行 Decision 的结果
        # - 不做判断、不做反思
        # - 只返回客观结果
        # -------------------------------------------------
        result = tool_func(step)

        # 保存原始执行结果（无论好坏）
        state.save(step, result)

        final_output += result["content"] + "\n"

        # -------------------------------------------------
        # 【Reflection Layer｜反思层】
        # - 比较「结果 vs 目标预期」
        # - 决定是否需要 Retry / 补充 / 停止
        # -------------------------------------------------
        reflection = reflect(step, result, state)

        if reflection.decision == ReflectionDecision.RETRY:
            print("→ 反思结果：需要重试或补充信息")
            # 这里暂时不实现 retry，只留下结构钩子
            # 企业项目中通常会在此触发二次 Decision

        elif reflection.decision == ReflectionDecision.CONTINUE:
            print("→ 反思结果：可以进入下一步")

        elif reflection.decision == ReflectionDecision.STOP:
            print("→ 反思结果：任务已满足，提前终止")
            break

    return final_output
