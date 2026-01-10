# agent/state.py
# State = Agent 的长期记忆 + 经验统计中心
# 为 Decision / Reflection 提供可决策数据

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
        self.history.append(record)

        if tool is None:
            return

        key = (step, tool)

        if success:
            self.success_count[key] = self.success_count.get(key, 0) + 1
            self.tool_success_count[tool] = self.tool_success_count.get(tool, 0) + 1
            # 成功：streak +1（如果之前是失败，则重置）
            self.streak_count[key] = max(1, self.streak_count.get(key, 0) + 1)
            self.tool_streak_count[tool] = max(1, self.tool_streak_count.get(tool, 0) + 1)
        else:
            self.failure_count[key] = self.failure_count.get(key, 0) + 1
            self.tool_failure_count[tool] = self.tool_failure_count.get(tool, 0) + 1
            # 失败：streak -1
            self.streak_count[key] = min(-1, self.streak_count.get(key, 0) - 1)
            self.tool_streak_count[tool] = min(-1, self.tool_streak_count.get(tool, 0) - 1)

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
        self.history.append(record)

        if tool is None:
            return

        key = (step, tool)

        if is_success:
            self.success_count[key] = self.success_count.get(key, 0) + 1
            self.streak_count[key] = max(1, self.streak_count.get(key, 0) + 1)
        else:
            self.failure_count[key] = self.failure_count.get(key, 0) + 1
            self.streak_count[key] = min(-1, self.streak_count.get(key, 0) - 1)
