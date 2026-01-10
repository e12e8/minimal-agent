# decision.py
# =========================================================
# 决策层 Decision
# 职责：
# - 只读信息：Step + State
# - 不执行工具
# - 计算每个候选工具的分数
# - 输出“最优工具选择”
# =========================================================

from agent.state import State


def choose_tool(step: str, state: State) -> str:
    """
    根据当前 Step 和 State，选择最合适的工具。

    评分规则（可解释）：
    - 成功次数带正权重（信任累积）
    - 失败次数带惩罚权重（避免不稳定工具）
    - streak 反映连续性（正为连续成功，负为连续失败）
    - 简单的 Step 关键词匹配可微调偏好
    """

    # 候选工具：保持与 agent.TOOL_MAP 中注册的工具一致
    candidate_tools = ["general", "tech"]

    scores = []
    for tool in candidate_tools:
        exp = state.get_experience(step, tool)

        # 基础分数（可调权重）
        score = 0.0
        score += exp.get("success", 0) * 2.0       # 成功次数加权
        score -= exp.get("failure", 0) * 1.5       # 失败次数惩罚
        score += exp.get("streak", 0) * 1.0        # 连续性影响（正/负）

        # 简单的 Step-工具相关性偏好
        if "技术" in step and tool == "tech":
            score += 1.0

        scores.append((score, tool))

    # 按分数排序并选择最高分工具
    scores.sort(reverse=True, key=lambda x: x[0])
    best_score, best_tool = scores[0]

    print(f"[Decision] Step='{step}' Tool Scores={scores} → 选择 {best_tool}")
    return best_tool
