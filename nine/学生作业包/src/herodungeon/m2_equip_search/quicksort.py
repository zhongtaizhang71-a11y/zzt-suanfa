"""M2 lesson 9: quicksort for equipment.

Implement ``quicksort_by`` yourself. Do not call ``sorted()``, ``list.sort()``
or any library sort.

Requirements:

* return a **new** list; never modify ``items``;
* ascending by ``key(item)``; ``descending=True`` gives the reverse order;
* pick the pivot with a rule that does **not** degrade on already-sorted input
  (median-of-three recommended: the median of ``low`` / ``mid`` / ``high``),
  and write your pivot rule in this docstring;
* quicksort is not stable; equal keys may come out in any order.

Events (``source=SOURCE``), one round of partitioning emits, in this order:

* ``partition``    the range being split (e.g. ``low``, ``high``, ``depth``)
* ``pivot``        the chosen pivot (e.g. ``pivot_index``, ``pivot_key``)
* ``compare``      every element compared against the pivot
* ``swap``         every exchange of two different positions
* ``place_pivot``  where the pivot finally lands

Pivot rule: median-of-three. For the range ``[low, high]`` we take the three
positions ``low``, ``mid = (low + high) // 2`` and ``high``, order those three
values with a fixed 3-comparison sorting network and use the middle one as the
pivot. On already-sorted input the median always lands near the centre, so the
recursion stays ``O(n log n)`` instead of degrading to ``O(n^2)`` like a
first/last-element pivot would. Partitioning is Lomuto: the pivot is swapped to
``high`` first, then every element ``< pivot`` is moved forward, and finally the
pivot is placed at its final index (the ``place_pivot`` event).
"""

from __future__ import annotations

from typing import Any, Callable, Sequence, TypeVar

from herodungeon.core.events import EventRecorder

T = TypeVar("T")
SOURCE = "m2.quicksort"


def quicksort_by(
    items: Sequence[T],
    key: Callable[[T], Any],
    recorder: EventRecorder | None = None,
    descending: bool = False,
) -> list[T]:
    """Return a new list sorted by ``key`` using quicksort."""
    if recorder is None:
        recorder = EventRecorder()

    data: list[T] = list(items)

    def less(a: T, b: T) -> bool:
        if descending:
            return key(a) > key(b)
        return key(a) < key(b)

    def median_index(low: int, high: int) -> int:
        mid = (low + high) // 2
        lo, mi, hi = low, mid, high
        if less(data[mi], data[lo]):
            lo, mi = mi, lo
        if less(data[hi], data[mi]):
            mi, hi = hi, mi
        if less(data[mi], data[lo]):
            lo, mi = mi, lo
        return mi

    def partition(low: int, high: int, depth: int) -> int:
        recorder.emit("partition", SOURCE, low=low, high=high, depth=depth)
        pivot_index = median_index(low, high)
        recorder.emit("pivot", SOURCE, pivot_index=pivot_index, pivot_key=key(data[pivot_index]))
        if pivot_index != high:
            data[pivot_index], data[high] = data[high], data[pivot_index]
            recorder.emit("swap", SOURCE, i=pivot_index, j=high)
            pivot_index = high
        store = low
        for i in range(low, high):
            recorder.emit("compare", SOURCE, index=i, pivot_index=pivot_index)
            if less(data[i], data[pivot_index]):
                if i != store:
                    data[i], data[store] = data[store], data[i]
                    recorder.emit("swap", SOURCE, i=i, j=store)
                store += 1
        if store != high:
            data[store], data[high] = data[high], data[store]
            recorder.emit("swap", SOURCE, i=store, j=high)
        recorder.emit("place_pivot", SOURCE, pivot_index=store)
        return store

    def sort_range(low: int, high: int, depth: int) -> None:
        if low >= high:
            return
        pivot = partition(low, high, depth)
        sort_range(low, pivot - 1, depth + 1)
        sort_range(pivot + 1, high, depth + 1)

    if data:
        sort_range(0, len(data) - 1, 0)
    return data
