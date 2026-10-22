"""M2 lesson 10: binary search and lower-bound over already-sorted equipment.

The input must already be sorted by ``key``. Ascending ``binary_search_by``
should be implemented via ``lower_bound_by`` so duplicate keys return the
*first* match. Do not scan from left to right.
"""

from __future__ import annotations

from typing import Any, Callable, Sequence, TypeVar

from herodungeon.core.events import EventRecorder

T = TypeVar("T")

SOURCE = "m2.binary_search"
SOURCE_LOWER = "m2.lower_bound"


def lower_bound_by(
    sorted_items: Sequence[T],
    target_key: Any,
    key: Callable[[T], Any],
    recorder: EventRecorder | None = None,
) -> int:
    """Return the first index whose key is ``>= target_key`` (ascending only).

    Returns ``0..n``. Use a closed interval ``lo..hi`` and an ``ans`` slot
    (same as lesson 8). Emit ``probe`` (with ``go_left``) and a final ``bound``.
    """
    recorder = recorder or EventRecorder()
    n = len(sorted_items)
    lo, hi, ans = 0, n - 1, n
    while lo <= hi:
        mid = (lo + hi) // 2
        mid_key = key(sorted_items[mid])
        go_left = mid_key >= target_key
        recorder.emit(
            "probe",
            SOURCE_LOWER,
            index=mid,
            key=mid_key,
            target=target_key,
            go_left=go_left,
        )
        if go_left:
            ans = mid
            hi = mid - 1
        else:
            lo = mid + 1
    recorder.emit("bound", SOURCE_LOWER, index=ans)
    return ans


def binary_search_by(
    sorted_items: Sequence[T],
    target_key: Any,
    key: Callable[[T], Any],
    recorder: EventRecorder | None = None,
    descending: bool = False,
) -> int:
    """Return the index of the first item whose key equals ``target_key``.

    Ascending (default): call ``lower_bound_by``, then check that cell.
    Return ``-1`` when no match exists. ``descending=True`` is optional.
    """
    recorder = recorder or EventRecorder()
    n = len(sorted_items)
    if not descending:
        index = lower_bound_by(sorted_items, target_key, key, recorder)
        if index < n and key(sorted_items[index]) == target_key:
            recorder.emit("found", SOURCE, index=index)
            return index
        recorder.emit("not_found", SOURCE, target=target_key)
        return -1
    lo, hi = 0, n - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        mid_key = key(sorted_items[mid])
        recorder.emit(
            "probe",
            SOURCE,
            index=mid,
            key=mid_key,
            target=target_key,
            go_left=mid_key < target_key,
        )
        if mid_key == target_key:
            recorder.emit("found", SOURCE, index=mid)
            return mid
        if mid_key > target_key:
            lo = mid + 1
        else:
            hi = mid - 1
    recorder.emit("not_found", SOURCE, target=target_key)
    return -1
