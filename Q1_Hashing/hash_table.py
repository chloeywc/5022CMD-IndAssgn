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

    # ---------- internal helpers ----------

    def _hash(self, key):
        """Map a key to its home slot index."""
        return hash(key) % self._capacity

    def _find_index(self, key):
        """Return the slot index holding key, or None if key is not stored."""
        start = self._hash(key)
        for i in range(self._capacity):
            index = (start + i) % self._capacity  # linear probing
            slot = self._slots[index]
            if slot is None:                      # empty slot: key cannot be further on
                return None
            if slot is not self._DELETED and slot.key == key:
                return index
        return None

    # ---------- public operations ----------

    def insert(self, key, value):
        """Insert a new key, or update it if it already exists. Returns the slot index."""
        existing = self._find_index(key)
        if existing is not None:              # key already stored: update, don't duplicate
            self._slots[existing].value = value
            return existing

        start = self._hash(key)
        for i in range(self._capacity):
            index = (start + i) % self._capacity
            slot = self._slots[index]
            if slot is None or slot is self._DELETED:  # reuse empty or deleted slots
                self._slots[index] = _Entry(key, value)
                self._size += 1
                return index

        raise OverflowError("Hash table is full")

    def search(self, key):
        """Return the value for key, or None if not found."""
        index = self._find_index(key)
        return None if index is None else self._slots[index].value

    def delete(self, key):
        """Remove key and return the slot index it was in, or None if not found."""
        index = self._find_index(key)
        if index is None:
            return None
        self._slots[index] = self._DELETED    # tombstone keeps probe chains intact
        self._size -= 1
        return index

    # ---------- information for display / analysis ----------

    def home_slot(self, key):
        """Return the slot a key would ideally go to (before any probing)."""
        return self._hash(key)

    def find_slot(self, key):
        """Return the slot index where key is stored, or None if not found."""
        return self._find_index(key)

    def slots(self):
        """Yield (index, status, key, value) for every slot in the table."""
        for index, slot in enumerate(self._slots):
            if slot is None:
                yield index, "EMPTY", None, None
            elif slot is self._DELETED:
                yield index, "DELETED", None, None
            else:
                yield index, "OCCUPIED", slot.key, slot.value

    def load_factor(self):
        """Fraction of slots currently in use (0.0 to 1.0)."""
        return self._size / self._capacity

    @property
    def capacity(self):
        return self._capacity

    def __len__(self):
        return self._size


if __name__ == "__main__":
    table = HashTable(capacity=10)
    print(table.insert(3, "A"))    # expect 3
    print(table.insert(13, "B"))   # collision -> expect 4
    print(table.insert(23, "C"))   # collision -> expect 5
    print(table.delete(13))        # expect 4 (slot 4 becomes a tombstone)
    print(table.search(23))        # expect C: tombstone lets the search continue
    print(table.insert(23, "C2"))  # expect 5: updates, does NOT duplicate into slot 4
    print(len(table))              # expect 2