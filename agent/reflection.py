# agent/reflection.py
# =========================================================
# Reflection = 反思层
# 职责：
# - 不执行工具
# - 不选择工具
# - 只评估“结果质量 + 是否可信 + 是否需要重试”
# - 产出结构化信号，供 State / Decision 使用
# =========================================================

from dataclasses import dataclass
from enum import Enum


# ===============================
# 失败原因枚举（用于决策降权）
# ===============================
class FailureReason(Enum):
    TOOL_MISMATCH = "tool_mismatch"   # 工具类型不适合该任务
    LOW_QUALITY = "low_quality"       # 输出质量低
    INCOMPLETE = "incomplete"         # 信息不完整
    UNKNOWN = "unknown"


# ===============================
# Reflection 的统一结构化输出
# ===============================
@dataclass
class ReflectionResult:
    is_success: bool                  # 是否认为本次执行成功
    confidence: float                 # 结果可信度（0~1）
    should_retry: bool                # 是否建议 Agent 重试
    reason: str                       # 反思理由（日志 / 可解释性）
    failure_reason: FailureReason | None = None


# ===============================
# Reflection 主函数
# ===============================
def reflect(step: str, result: dict, state) -> ReflectionResult:
    """
    对工具执行结果进行反思评估
    Reflection 只做判断，不修改状态
    """

    content = result.get("content", "")
    tool = result.get("tool")

    # -------------------------------------------------
    # 1. 基础有效性判断
    # -------------------------------------------------
    if not content or len(content.strip()) < 10:
        return ReflectionResult(
            is_success=False,
            confidence=0.2,
            should_retry=True,
            reason="输出内容过短，信息不足",
            failure_reason=FailureReason.INCOMPLETE
        )

    # -------------------------------------------------
    # 2. 结合历史经验判断工具是否不适合
    #    注意：这里使用 tool 级经验，而非 step 级
    # -------------------------------------------------
    exp = state.get_experience(step, tool)

    # 连续失败说明 tool 与该类任务可能不匹配
    if exp.get("streak", 0) <= -2:
        return ReflectionResult(
            is_success=False,
            confidence=0.35,
            should_retry=True,
            reason="该工具在近期多次失败，可能不适合此类任务",
            failure_reason=FailureReason.TOOL_MISMATCH
        )

    # -------------------------------------------------
    # 3. 成功但质量一般（可选扩展）
    # -------------------------------------------------
    if len(content.strip()) < 50:
        return ReflectionResult(
            is_success=True,
            confidence=0.6,
            should_retry=False,
            reason="结果基本可用，但信息密度偏低",
            failure_reason=None
        )

    # -------------------------------------------------
    # 4. 正常成功
    # -------------------------------------------------
    return ReflectionResult(
        is_success=True,
        confidence=0.85,
        should_retry=False,
        reason="结果完整，历史表现良好",
        failure_reason=None
    )
