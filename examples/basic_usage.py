"""AML SDK 基础使用示例"""

from aml import AMLNode

# 创建 AML 节点
node = AMLNode()

# 对话示例
response = node.chat("你好，AI 文明")
print(f"响应: {response}")

# 语义蒸馏示例
vsc_seq = node.distill("打印高清图片")
print(f"VSC 序列: {vsc_seq}")

# 编码传输示例
encoded = node.encode(vsc_seq)
print(f"编码后大小: {len(encoded)} bytes")

# 解码示例
decoded = node.decode(encoded)
print(f"解码后 VSC 序列: {decoded}")
