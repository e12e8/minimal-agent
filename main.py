"""
主运行脚本：调用 `run_agent` 启动简约 Agent，示例展示基本运行流程。
"""

from agent.agent import run_agent


if __name__ == "__main__":
    # 启动 Agent 并打印最终汇总输出（用于演示和手动测试）
    output = run_agent("解释 Agent 的基本运行机制")
    print("\n=== 最终输出 ===")
    print(output)
