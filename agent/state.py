# state.py
# State 用来保存执行过程中的中间结果（轻量级存储）


class State:
    """
    简单的状态容器，用于在 Agent 执行过程中保存每一步的结果。

    属性:
        memory (dict): 以步骤描述为键、工具返回结果为值的字典
    """

    def __init__(self):
        # 初始化一个空字典作为内存存储
        self.memory = {}

    def save(self, step: str, result: dict):
        """
        将某一步的执行结果保存到内存中。

        参数:
            step (str): 步骤描述，用作键
            result (dict): 工具或执行单元返回的结果字典
        """
        self.memory[step] = result

    def get(self, step: str):
        """
        从内存中获取某一步的结果，找不到返回 None。

        参数:
            step (str): 目标步骤描述

        返回:
            dict | None: 对应步骤的结果或 None
        """
        return self.memory.get(step)
