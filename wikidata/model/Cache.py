from collections import deque

class Cache:
    """

    """

    def __init__(self, max_size: int):
        self.size = 0
        self.cache_max_size = max_size

        self.keys = deque(list(), max_size)
        self.map = dict()

    def add(self, key, value):
        if self.size == self.cache_max_size:
            old_key = self.keys.popleft()
            del self.map[old_key]
        else:
            self.size += 1

        self.map[key] = value
        self.keys.append(key)

    def get(self, key: str):
        if key in self.map:
            return self.map[key]

        return None

