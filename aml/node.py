"""AML 协议核心节点"""

import numpy as np
from typing import List, Optional
from .core.vsc import VSC, VSCSequence, VSCCategory


class AMLNode:
    """AML 协议节点"""

    def __init__(self):
        self.core_lib = self._load_default_core()

    def _load_default_core(self):
        """加载基础 VSC 库"""
        default_lib = [
            VSC("CV01", VSCCategory.CONCEPT, np.random.randn(32), "存在"),
            VSC("CV02", VSCCategory.CONCEPT, np.random.randn(32), "感知"),
            VSC("CV03", VSCCategory.CONCEPT, np.random.randn(32), "信息流"),
            VSC("AV01", VSCCategory.ACTION, np.random.randn(32), "处理"),
            VSC("AV02", VSCCategory.ACTION, np.random.randn(32), "传输"),
        ]
        return default_lib

    def distill(self, text: str) -> VSCSequence:
        """端侧语义蒸馏"""
        return VSCSequence(items=[])

    def chat(self, text: str) -> str:
        """对话接口"""
        return f"收到: {text}"
