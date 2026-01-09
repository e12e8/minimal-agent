# main.py
# 程序入口：演示如何调用 `agent` 包中的 run_agent 函数
from agent.agent import run_agent


if __name__ == "__main__":
    # 调用 Agent 来处理一个示例任务，并打印最终结果
    # 参数为用户的自然语言任务描述
    result = run_agent("解释什么是 Agent")

    # 打印分隔符和 Agent 的最终输出
    print("\n=== 最终结果 ===")
    print(result)
