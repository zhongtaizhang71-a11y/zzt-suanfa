"""M1 lesson 3: implement the list-based inventory.

Replace every `NotImplementedError` below. Do not change the public method
names or the exception types — the tests depend on them.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from herodungeon.core.events import AlgorithmEvent, EventRecorder
from herodungeon.core.models import Item


class InventoryFullError(ValueError):
    pass


class ItemNotFoundError(KeyError):
    pass


@dataclass(slots=True)
class Inventory:
    capacity: int
    recorder: EventRecorder = field(default_factory=EventRecorder)
    _items: list[Item] = field(default_factory=list, init=False, repr=False)

    def __post_init__(self) -> None:
        if self.capacity <= 0:
            raise ValueError("capacity must be positive")

    @property
    def items(self) -> tuple[Item, ...]:
        return tuple(self._items)

    def add(self, item: Item) -> AlgorithmEvent:
        """Append `item` if there is room; otherwise reject and raise."""
        if len(self._items) >= self.capacity:
            self.recorder.emit("reject", "inventory", item_id=item.item_id)
            raise InventoryFullError(f"inventory full: cannot add {item.item_id!r}")
        if any(existing.item_id == item.item_id for existing in self._items):
            raise ValueError(f"duplicate item_id: {item.item_id!r}")
        self._items.append(item)
        return self.recorder.emit("insert", "inventory", item_id=item.item_id)

    def remove(self, item_id: str) -> Item:
        """Find `item_id` from the front, emit compare/remove/miss, and return it."""
        for index, current in enumerate(self._items):
            self.recorder.emit(
                "compare", "inventory", index=index, item_id=current.item_id
            )
            if current.item_id == item_id:
                self._items.pop(index)
                self.recorder.emit("remove", "inventory", item_id=item_id)
                return current
        self.recorder.emit("miss", "inventory", item_id=item_id)
        raise ItemNotFoundError(item_id)

    def total_value(self) -> int:
        """Return the sum of item values currently in the bag."""
        return sum(item.value for item in self._items)
