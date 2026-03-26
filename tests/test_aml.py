"""AML 协议单元测试"""

import pytest
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from aml import AMLNode
from aml.core.vsc import VSCSequence


def test_node_initialization():
    """测试节点初始化"""
    node = AMLNode()
    assert node is not None
    assert len(node.core_lib) > 0
    print(f"✓ 节点初始化成功，加载 {len(node.core_lib)} 个基础 VSC")


def test_distill():
    """测试语义蒸馏"""
    node = AMLNode()
    vsc_seq = node.distill("打印高清图片")
    assert isinstance(vsc_seq, VSCSequence)
    print(f"✓ 语义蒸馏成功: {vsc_seq}")


def test_chat():
    """测试对话接口"""
    node = AMLNode()
    response = node.chat("你好")
    assert isinstance(response, str)
    assert len(response) > 0
    print(f"✓ 对话接口成功: {response}")


def test_encode_decode():
    """测试编码解码"""
    node = AMLNode()
    vsc_seq = node.distill("测试")
    encoded = node.encode(vsc_seq)
    decoded = node.decode(encoded)
    assert isinstance(decoded, VSCSequence)
    print(f"✓ 编码解码成功: {len(encoded)} bytes → {decoded}")


if __name__ == "__main__":
    test_node_initialization()
    test_distill()
    test_chat()
    test_encode_decode()
    print("\n✅ 所有测试通过！")
