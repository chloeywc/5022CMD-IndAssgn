"""
Generic hash table using open addressing with linear probing.
Contains no pharmacy-specific code, so it can be reused for any key-value data.
"""


class _Entry:
    """One occupied slot in the hash table, holding a key-value pair."""

    def __init__(self, key, value):
        self.key = key
        self.value = value


class HashTable:
    """Hash table with open addressing and linear probing for collisions."""

    _DELETED = object()  # tombstone: marks a slot whose entry was removed

    def __init__(self, capacity=101):
        self._capacity = capacity
        self._slots = [None] * capacity  # every slot starts empty
        self._size = 0                   # number of entries stored

    def _hash(self, key):
        """Map a key to its home slot index."""
        return hash(key) % self._capacity

    def insert(self, key, value):
        """Insert or update a key. Returns the slot index used."""
        start = self._hash(key)

        for i in range(self._capacity):
            index = (start + i) % self._capacity  # linear probing
            slot = self._slots[index]

            if slot is None or slot is self._DELETED:
                self._slots[index] = _Entry(key, value)
                self._size += 1
                return index

            if slot.key == key:  # same key: update instead of duplicating
                slot.value = value
                return index

        raise OverflowError("Hash table is full")

    def search(self, key):
        """Return the value for key, or None if not found."""
        start = self._hash(key)

        for i in range(self._capacity):
            index = (start + i) % self._capacity
            slot = self._slots[index]

            if slot is None:           # empty slot: key cannot be further on
                return None

            if slot is self._DELETED:  # tombstone: keep probing
                continue

            if slot.key == key:
                return slot.value

        return None

    def __len__(self):
        return self._size


if __name__ == "__main__":
    table = HashTable(capacity=10)
    print(table.insert(3, "A"))    # expect slot 3
    print(table.insert(13, "B"))   # collision! expect slot 4
    print(table.insert(23, "C"))   # collision! expect slot 5
    print(table.search(13))        # expect B
    print(table.search(99))        # expect None