# Vaishnavi Ladda PRN:21610076
class BloomFilter:
    def __init__(self, filter_size):
        self.filter_size = filter_size
        self.bit_set = [False] * filter_size

    def add(self, key):
        hash1 = self.hash_function1(key)
        hash2 = self.hash_function2(key)
        hash3 = self.hash_function3(key)
        self.bit_set[hash1] = True
        self.bit_set[hash2] = True
        self.bit_set[hash3] = True

    def contains(self, key):
        hash1 = self.hash_function1(key)
        hash2 = self.hash_function2(key)
        hash3 = self.hash_function3(key)
        return self.bit_set[hash1] and self.bit_set[hash2] and self.bit_set[hash3]

    def hash_function1(self, key):
        x = int(key)
        return (3 * x + 1) % self.filter_size

    def hash_function2(self, key):
        x = int(key)
        return (3 * x + 5) % (self.filter_size - 1)  # Use filter_size - 1 as the divisor

    def hash_function3(self, key):
        x = int(key)
        return (3 * x + 7) % (self.filter_size - 2)  # Use filter_size - 2 as the divisor


def bloom_join(relation1, relation2):
    FILTER_SIZE = 10
    bloom_filter = BloomFilter(FILTER_SIZE)
    for row in relation2:
        parts = row.split(",")
        key = parts[0].strip()
        bloom_filter.add(key)

    result = []
    for row in relation1:
        parts = row.split(",")
        key = parts[0].strip()
        if bloom_filter.contains(key):
            result.append(row)

    return result


if __name__ == "__main__":
    relation1 = [
        "201, John",
        "202, Alice",
        "203, Bob",
        "204, Charlie",
        "205, David",
    ]
    relation2 = [
        "201, Engineering",
        "202, Sales",
        "204, Marketing",
        "206, HR",
        "207, Finance",
    ]

    # Perform Bloom join
    result = bloom_join(relation1, relation2)

    # Print result
    for row in result:
        print(row)