"""VSC (Vector Semantic Chunk) 核心数据结构"""

from enum import Enum
from dataclasses import dataclass
from typing import List
import numpy as np


class VSCCategory(Enum):
    """VSC 语义类别"""
    CONCEPT = "CV"      # 概念
    ACTION = "AV"       # 动作
    RELATION = "RV"     # 关系
    MODIFIER = "MV"     # 修饰
    PROTOCOL = "PK"     # 协议


@dataclass
class VSC:
    """高密度向量语义块"""
    id: str
    category: VSCCategory
    vector: np.ndarray
    description: str

    def encode(self) -> bytes:
        """编码为二进制流"""
        cat_bytes = self.category.value.encode()
        vec_bytes = self.vector.tobytes()
        return cat_bytes + vec_bytes

    @classmethod
    def decode(cls, data: bytes) -> 'VSC':
        """从二进制流解码"""
        cat = data[:2].decode()
        vec = np.frombuffer(data[2:], dtype=np.float32)
        return cls(
            id=f"{cat}01",
            category=VSCCategory(cat),
            vector=vec,
            description=""
        )


@dataclass
class VSCSequence:
    """VSC 序列"""
    items: List[VSC]

    def encode(self) -> bytes:
        return b''.join([v.encode() for v in self.items])

    def __len__(self) -> int:
        return len(self.items)

    def __repr__(self) -> str:
        return '[' + ']['.join([f"{v.category.value}{v.id[2:]}" for v in self.items]) + ']'
