# agent/reflection.py
# Reflection = 结果评估层
# 作用：不执行、不决策，只做“结果质量判断 & 经验修正建议”

from dataclasses import dataclass


@dataclass
class ReflectionDecision:
    """
    Reflection 的结构化输出
    """
    is_success: bool           # 这次是否算成功
    confidence: float          # 对结果的信任程度（0~1）
    should_retry: bool         # 是否建议重试
    reason: str                # 判断原因（用于日志 / 面试讲解）


def reflect(step: str, result: dict, state) -> ReflectionDecision:
    """
    对工具执行结果进行反思评估
    """

    content = result.get("content", "")
    tool = result.get("tool")

    # 1. 最基础判断：是否有有效输出
    if not content or len(content.strip()) < 10:
        return ReflectionDecision(
            is_success=False,
            confidence=0.2,
            should_retry=True,
            reason="输出内容过短，信息不足",
        )

    # 2. 结合历史经验判断可信度
    exp = state.get_experience(step, tool)

    # 如果这个 tool 在这个 step 上连续失败过
    if exp["streak"] < -1:
        return ReflectionDecision(
            is_success=False,
            confidence=0.3,
            should_retry=True,
            reason="该工具在此步骤上近期连续失败",
        )

    # 3. 正常成功情况
    return ReflectionDecision(
        is_success=True,
        confidence=0.8,
        should_retry=False,
        reason="结果完整且历史表现正常",
    )
