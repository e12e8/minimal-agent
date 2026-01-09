# State：跨 Step 的长期记忆
# 不做决策，只存储事实（包括工具结果和 reflection 的判断）


class State:
    """
    轻量级历史记录容器，用于保存每一步的执行结果和反思信息。
    """

    def __init__(self):
        # history 列表按执行顺序保存每一步的记录
        self.history = []

    def save(self, step, result, reflection):
        """
        保存当前步骤的执行结果与 reflection 信息，供审计或后续决策使用。
        """
        self.history.append({
            "step": step,
            "result": result,
            "reflection": reflection
        })
