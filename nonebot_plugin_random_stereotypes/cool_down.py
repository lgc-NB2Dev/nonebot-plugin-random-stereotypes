import time
from collections import defaultdict, deque
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Deque, Dict, Optional

from .config import config


@dataclass
class CoolingDownError(Exception):
    time_left: float
    queried_count_when_cooling: int
    punished: bool


# 用户在 cool_down_query_count_time 内 visit cool_down_query_count 次，计算为冷却
# 冷却后继续 visit 达到 punish_query_count 次后，则判定为恶意行为，冷却时间重置
@dataclass
class CoolDownManager:
    cool_down_time: float
    cool_down_query_count: int
    cool_down_query_count_time: int
    punish_query_count: int

    def __post_init__(self):
        self.cool_times: Dict[str, Deque[float]] = defaultdict(
            lambda: deque(maxlen=self.punish_query_count),
        )
        self.queried_counts_when_cooling: Dict[str, int] = defaultdict(lambda: 0)

    def append(self, key: str):
        now = time.time()
        self.cool_times[key].append(now)
        return now

    def punish(self, key: str):
        now = time.time()
        self.cool_times[key].extend(now for _ in range(self.cool_down_query_count))

    def check_time_left_only(self, key: str) -> Optional[float]:
        if (
            (key not in self.cool_times)
            or (len((deq := self.cool_times[key])) < self.cool_down_query_count)
            or (deq[-1] - deq[0] > self.cool_down_query_count_time)
        ):
            return None
        time_left = self.cool_down_time - (time.time() - deq[-1])
        return time_left if time_left > 0 else None

    def visit(self, key: str):
        time_left = self.check_time_left_only(key)
        if time_left:
            self.queried_counts_when_cooling[key] += 1
            should_punish = (
                self.queried_counts_when_cooling[key] >= self.punish_query_count
            )
            if should_punish:
                self.punish(key)
            raise CoolingDownError(
                # self.cool_down_time if should_punish else time_left,
                time_left,
                self.queried_counts_when_cooling[key],
                should_punish,
            )
        if key in self.queried_counts_when_cooling:
            del self.queried_counts_when_cooling[key]

    def ctx(self, key: str):
        self.visit(key)

        @contextmanager
        def _ctx():
            last_cool = self.cool_times.get(key)
            now_cool = self.append(key)  # 冷却占位
            try:
                yield
            except Exception:
                if last_cool:
                    self.cool_times[key] = last_cool
                else:
                    del self.cool_times[key]
                raise
            else:
                # 把预先占位的冷却时间 del 重新 append
                deq = self.cool_times[key]
                idx = next(
                    (i for i in range(len(deq) - 1, -1, -1) if deq[i] == now_cool),
                    None,
                )
                if idx is not None:
                    del deq[idx]
                    self.append(key)

        return _ctx()


cool_down = CoolDownManager(
    config.stereotypes_cd,
    config.stereotypes_count,
    config.stereotypes_count_time,
    config.stereotypes_punish_count,
)
