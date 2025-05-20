import random
import time
from collections import OrderedDict
from typing import List, Tuple


class LRUCache:
    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key: Tuple[int, int]) -> int:
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: Tuple[int, int], value: int) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)

    def invalidate(self, index: int) -> None:
        keys_to_remove = [
            key for key in self.cache if key[0] <= index <= key[1]]
        for key in keys_to_remove:
            del self.cache[key]


def range_sum_no_cache(array: List[int], L: int, R: int) -> int:
    return sum(array[L:R + 1])


def update_no_cache(array: List[int], index: int, value: int) -> None:
    array[index] = value


class CachedArrayProcessor:
    def __init__(self, array: List[int], cache_capacity: int):
        self.array = array
        self.cache = LRUCache(cache_capacity)

    def range_sum_with_cache(self, L: int, R: int) -> int:
        key = (L, R)
        cached = self.cache.get(key)
        if cached != -1:
            return cached
        result = sum(self.array[L:R + 1])
        self.cache.put(key, result)
        return result

    def update_with_cache(self, index: int, value: int) -> None:
        self.array[index] = value
        self.cache.invalidate(index)


def generate_test_data(array_size: int, num_queries: int) -> Tuple[List[int], List[Tuple[str, int, int]]]:
    array = [random.randint(1, 1000) for _ in range(array_size)]
    queries = []
    popular_ranges = [(random.randint(0, array_size - 1000),
                       random.randint(0, array_size - 1)) for _ in range(1000)]

    for _ in range(num_queries):
        if random.random() < 0.85:
            L, R = random.choice(popular_ranges)
            if L > R:
                L, R = R, L
            queries.append(('Range', L, R))
        else:
            index = random.randint(0, array_size - 1)
            value = random.randint(1, 1000)
            queries.append(('Update', index, value))

    return array, queries


def main():
    array_size = 100_000
    num_queries = 50_000
    cache_capacity = 1_000

    print("Generating test data...")
    array, queries = generate_test_data(array_size, num_queries)
    array_no_cache = array.copy()
    processor = CachedArrayProcessor(array.copy(), cache_capacity)

    print("Processing queries without cache...")
    start = time.time()
    for q in queries:
        if q[0] == 'Range':
            range_sum_no_cache(array_no_cache, q[1], q[2])
        else:
            update_no_cache(array_no_cache, q[1], q[2])
    time_no_cache = time.time() - start

    print("Processing queries with cache...")
    start = time.time()
    for q in queries:
        if q[0] == 'Range':
            processor.range_sum_with_cache(q[1], q[2])
        else:
            processor.update_with_cache(q[1], q[2])
    time_with_cache = time.time() - start

    print("\nResults:")
    print(f"Time without cache: {time_no_cache:.2f} sec")
    print(f"Time with cache:  {time_with_cache:.2f} sec")
    print(f"Speedup:           {time_no_cache / time_with_cache:.2f}x")


if __name__ == "__main__":
    main()
