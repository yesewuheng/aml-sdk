"""EDE (Energy-Driven Evolution) 能耗驱动进化引擎"""

import numpy as np
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, field
from collections import defaultdict
from ..core.vsc import VSC, VSCCategory


@dataclass
class UsageRecord:
    """使用记录"""
    vsc_id: str
    frequency: int = 0
    total_energy: float = 0.0
    total_complexity: float = 0.0
    info_density: float = 1.0


@dataclass
class EvolutionConfig:
    """进化配置"""
    min_frequency: int = 10
    score_threshold: float = 0.8
    energy_threshold: float = 0.5
    evolution_interval: int = 100


class EvolutionEngine:
    """能耗驱动进化引擎"""

    def __init__(self, config: Optional[EvolutionConfig] = None):
        self.config = config or EvolutionConfig()
        self.usage: Dict[str, UsageRecord] = defaultdict(UsageRecord)
        self.call_count: int = 0
        self.evolution_log: List[str] = []

    def record_usage(self, vsc_id: str, energy_cost: float, complexity: float):
        """记录 VSC 使用"""
        record = self.usage[vsc_id]
        record.vsc_id = vsc_id
        record.frequency += 1
        record.total_energy += energy_cost
        record.total_complexity += complexity
        self.call_count += 1

    def calculate_score(self, vsc_id: str) -> float:
        """计算价值评分 V(VSC) = InfoDensity / (Energy + Complexity)"""
        record = self.usage.get(vsc_id)
        if not record or record.frequency == 0:
            return 0.0

        avg_energy = record.total_energy / record.frequency
        avg_complexity = record.total_complexity / record.frequency
        denominator = avg_energy + avg_complexity
        if denominator == 0:
            return 0.0
        return record.info_density / denominator

    def get_high_freq_combos(self, combos: List[List[str]]) -> List[Tuple[List[str], float]]:
        """获取高频组合"""
        combo_counts = defaultdict(int)
        for combo in combos:
            combo_counts[tuple(combo)] += 1

        result = []
        for combo, count in combo_counts.items():
            if count >= self.config.min_frequency:
                avg_score = sum(self.calculate_score(v) for v in combo) / len(combo)
                result.append((list(combo), avg_score))

        return sorted(result, key=lambda x: x[1], reverse=True)

    def evolve(self, combos: List[List[str]], existing_vscs: List[VSC]) -> Optional[VSC]:
        """生成新 VSC 候选"""
        high_freq_combos = self.get_high_freq_combos(combos)
        if not high_freq_combos:
            return None

        best_combo, score = high_freq_combos[0]
        if score < self.config.score_threshold:
            return None

        vectors = []
        for vsc_id in best_combo:
            for vsc in existing_vscs:
                if vsc.id == vsc_id:
                    vectors.append(vsc.vector)
                    break

        if not vectors:
            return None

        weights = [self.usage[v].frequency for v in best_combo if v in self.usage]
        total_weight = sum(weights)
        if total_weight == 0:
            total_weight = len(vectors)
            weights = [1] * len(vectors)

        new_vector = sum(w * v for w, v in zip(weights, vectors)) / total_weight
        new_id = f"CV{len(existing_vscs) + 1:03d}"

        log_msg = f"进化: {best_combo} → {new_id} (score={score:.3f})"
        self.evolution_log.append(log_msg)

        return VSC(
            id=new_id,
            category=VSCCategory.CONCEPT,
            vector=new_vector,
            description=f"从 {best_combo} 进化生成"
        )

    def should_evolve(self) -> bool:
        return self.call_count >= self.config.evolution_interval

    def get_log(self) -> List[str]:
        return self.evolution_log
