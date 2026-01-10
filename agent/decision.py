# decision.py
# Decision = 决策层
# 职责：根据 Step + State，选择当前最合适的 Tool
# ⚠️ 不执行 Tool，不关心结果，只做“策略选择”

from agent.state import State


def choose_tool(step: str, state: State) -> str:
    """
    根据当前 step 和历史 state，选择最优工具

    策略（工程可解释）：
    - 连续成功（streak）权重最高
    - 失败次数是强烈惩罚
    """

    # 当前 Agent 支持的工具集合（可扩展）
    candidate_tools = ["general", "tech"]

    scored_tools = []

    for tool in candidate_tools:
        exp = state.get_experience(step, tool)

        # 基础分：没有历史就从 0 开始
        score = 0

        if exp:
            # 连续成功是“信任建立”的核心
            score += exp["streak"] * 2

            # 失败是强惩罚（工程上避免不稳定工具）
            score -= exp["failure"] * 3

        scored_tools.append((score, tool))

    # 按 score 从高到低排序
    scored_tools.sort(reverse=True, key=lambda x: x[0])

    # 返回得分最高的工具
    selected_tool = scored_tools[0][1]

    # 调试输出（强烈建议保留，面试可演示）
    print(f"[Decision] Step='{step}' Tool Scores={scored_tools} → 选择 {selected_tool}")

    return selected_tool
