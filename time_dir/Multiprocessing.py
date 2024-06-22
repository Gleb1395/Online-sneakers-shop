import random
import time

import multiprocess


class timer:
    def __init__(self, message):
        self.message = message

    def __enter__(self):
        self.start = time.time()
        return None

    def __exit__(self, type, value, traceback):
        elapsed_time = time.time() - self.start
        print(self.message.format(elapsed_time))


workers = 4
DATA_SIZE = 1_000_000
lst = []


def fill_data(n):
    while n > 0:
        n -= 1
        lst.append(random.randint(1, 100))


if __name__ == "__main__":
    with timer("Elapsed: {}s"):
        with multiprocess.Pool(workers) as pool:
            input_data = [DATA_SIZE // workers for _ in range(workers)]
            pool.map(fill_data, input_data)

# 1 - 0.73
# 2 - 0.40
# 3 - 0.34
# 4 - 0.42
