"""M1 lesson 6: sliding window over the recent combat damage log.

Do not recompute each window from scratch. Slide by subtracting the leaving
value and adding the entering value so the whole scan is O(n).
"""

from __future__ import annotations

from typing import Any, Sequence

from herodungeon.core.events import EventRecorder

SOURCE = "m1.sliding_window"


def _validate(damage_log: Sequence[int], size: int) -> None:
    if size <= 0:
        raise ValueError("window size must be positive")
    if size > len(damage_log):
        raise ValueError(
            f"window size {size} exceeds damage log length {len(damage_log)}"
        )


def max_damage_window(
    damage_log: Sequence[int],
    size: int,
    recorder: EventRecorder | None = None,
) -> tuple[int, int]:
    """Return ``(start_index, window_sum)`` of the highest-damage window.

    Ties must keep the earliest window.
    """
    _validate(damage_log, size)
    recorder = recorder or EventRecorder()

    # 第一个窗口：从头求和
    current_sum = sum(damage_log[:size])
    best_start = 0
    best_sum = current_sum
    recorder.emit(
        "window_init",
        SOURCE,
        start=0,
        end=size,
        values=list(damage_log[:size]),
        window_sum=current_sum,
    )

    # 窗口右移：减离开、加进入，O(n) 扫描
    for i in range(1, len(damage_log) - size + 1):
        leaving = damage_log[i - 1]
        entering = damage_log[i + size - 1]
        current_sum = current_sum - leaving + entering
        recorder.emit(
            "window_slide",
            SOURCE,
            start=i,
            end=i + size,
            leaving=leaving,
            entering=entering,
            window_sum=current_sum,
        )
        # 严格更大才更新，平局保留更早的窗口
        if current_sum > best_sum:
            best_sum = current_sum
            best_start = i

    recorder.emit(
        "window_best", SOURCE, best_start=best_start, best_sum=best_sum
    )
    return best_start, best_sum


def window_states(
    damage_log: Sequence[int], size: int
) -> list[dict[str, Any]]:
    """Return every window as {start, end, values, window_sum}."""
    _validate(damage_log, size)
    states: list[dict[str, Any]] = []

    # 第一个窗口
    current_sum = sum(damage_log[:size])
    states.append(
        {
            "start": 0,
            "end": size,
            "values": list(damage_log[:size]),
            "window_sum": current_sum,
        }
    )

    # 滑动生成后续窗口
    for i in range(1, len(damage_log) - size + 1):
        current_sum = current_sum - damage_log[i - 1] + damage_log[i + size - 1]
        states.append(
            {
                "start": i,
                "end": i + size,
                "values": list(damage_log[i : i + size]),
                "window_sum": current_sum,
            }
        )

    return states
