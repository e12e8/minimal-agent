# agent/state.py
# State = Agent 的长期记忆 + 经验统计中心
# 为 Decision / Reflection 提供可决策数据

from collections import defaultdict

class State:
    def __init__(self):
        # 完整执行历史（用于调试 / 反思）
        self.history = []

        # (step, tool) -> 成功 / 失败次数
        self.success_count = {}
        self.failure_count = {}

        # (step, tool) -> 连续成功或失败次数（正=成功，负=失败）
        self.streak_count = {}

        # tool -> 累计成功 / 失败次数（跨 Step 继承的统计）
        self.tool_success_count = {}
        self.tool_failure_count = {}

        # tool -> 连续成功/失败趋势（用于短期信号）
        self.tool_streak_count = {}
        # tool -> reason -> count，用于记录失败原因画像
        # 结构：tool -> { reason: count }
        self.tool_failure_reasons = defaultdict(lambda: defaultdict(int))

    def save(self, step: str, result: dict):
        """
        保存一次 Step 的执行结果
        """
        tool = result.get("tool")
        success = result.get("success", False)

        record = {
            "step": step,
            "tool": tool,
            "success": success,
            "content": result.get("content", ""),
        }
        # 仅记录原始执行历史；成功/失败统计由 Reflection 的 apply_reflection 负责
        self.history.append(record)

    def get_experience(self, step: str, tool: str) -> dict:
        """
        Decision 层唯一允许调用的经验接口
        """
        key = (step, tool)
        # 跨 Step 继承失败经验：将 per-key 与 tool 级别统计合并
        per_key_success = self.success_count.get(key, 0)
        per_key_failure = self.failure_count.get(key, 0)
        per_key_streak = self.streak_count.get(key, 0)

        tool_success = self.tool_success_count.get(tool, 0)
        tool_failure = self.tool_failure_count.get(tool, 0)
        tool_streak = self.tool_streak_count.get(tool, 0)

        combined_success = per_key_success + max(0, tool_success - per_key_success)
        combined_failure = per_key_failure + max(0, tool_failure - per_key_failure)

        # 合并 streak：优先使用 step 级别（更精细），否则回退到 tool 级别
        combined_streak = per_key_streak if per_key_streak != 0 else tool_streak

        return {
            "success": combined_success,
            "failure": combined_failure,
            "streak": combined_streak,
        }

    def get_tool_score(self, step: str, tool: str) -> int:
        """
        综合评分：长期经验 + 短期趋势
        """
        key = (step, tool)

        key = (step, tool)

        # 直接计算合并统计，避免循环调用 get_experience
        per_key_success = self.success_count.get(key, 0)
        per_key_failure = self.failure_count.get(key, 0)
        per_key_streak = self.streak_count.get(key, 0)

        tool_success = self.tool_success_count.get(tool, 0)
        tool_failure = self.tool_failure_count.get(tool, 0)
        tool_streak = self.tool_streak_count.get(tool, 0)

        success = per_key_success + max(0, tool_success - per_key_success)
        failure = per_key_failure + max(0, tool_failure - per_key_failure)
        streak = per_key_streak if per_key_streak != 0 else tool_streak

        return success - failure + streak * 2

    def record(self, step: str, tool: str, is_success: bool, reason: str = ""):
        """
        由 Reflection 层调用的记录方法。
        更新历史与统计（与 `save` 保持一致的统计逻辑），
        但接口更简单：直接传入 step/tool/is_success。
        """
        record = {
            "step": step,
            "tool": tool,
            "success": bool(is_success),
            "content": "",
            "source": "reflection",
            "reason": reason,
        }
        # 仅把反思记录加入历史；实际的成功/失败统计应当通过 apply_reflection 写入
        self.history.append(record)
        return

    def record_reflection(self, tool_name: str, reflection) -> None:
        """
        Reflection 层专用的失败画像记录接口。
        当 reflection 表示失败且包含原因时，累加 tool_failure_reasons。
        """
        if not reflection:
            return

        # 使用 ReflectionDecision 的字段名 `is_success` 与 `reason`
        if not getattr(reflection, "is_success", True):
            failure_reason = getattr(reflection, "reason", None)
            if failure_reason:
                self.tool_failure_reasons[tool_name][failure_reason] += 1

    def apply_reflection(self, step: str, tool: str, reflection) -> None:
        """
        将 Reflection 的结果写入 State。
        这是 Agent 形成经验的唯一入口（State 只负责记账，不做判断）。

        参数:
        - step: 当前步骤标识（用于可能的扩展记录）
        - tool: 工具名
        - reflection: ReflectionDecision 实例，包含 `is_success` 与 `reason`
        """

        # 初始化 tool 级统计（向后兼容）
        if tool not in self.tool_success_count:
            self.tool_success_count[tool] = 0
            self.tool_failure_count[tool] = 0
            self.tool_streak_count[tool] = 0

        # 只以 reflection 的判断为准，State 不二次判断
        if getattr(reflection, "is_success", False):
            self.tool_success_count[tool] = self.tool_success_count.get(tool, 0) + 1
            # 连续性计数：正数表示连续成功
            self.tool_streak_count[tool] = max(0, self.tool_streak_count.get(tool, 0)) + 1
        else:
            self.tool_failure_count[tool] = self.tool_failure_count.get(tool, 0) + 1
            # 连续性计数：负数表示连续失败
            self.tool_streak_count[tool] = min(0, self.tool_streak_count.get(tool, 0)) - 1

        # 如果 reflection 给出了失败原因，也记录到失败画像中
        failure_reason = getattr(reflection, "reason", None)
        if not getattr(reflection, "is_success", True) and failure_reason:
            self.tool_failure_reasons[tool][failure_reason] += 1
