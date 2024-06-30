# 1. Знайти точку оптимуму для задачі з картинками.
# 2. Знайти точку оптимуму для задачі зі списком.
# 3. Додаткове питання. Чи можуть бути об'єкти ключами в словнику і чому? Відповісти тут але додати як текстовий файл.
#
# !!! Результат в якості таблички. Google, excel як завгодно.
import os
import random
import string
import time
from multiprocessing.pool import ThreadPool

import multiprocess
import requests


class timer:
    def __init__(self, message):
        self.message = message

    def __enter__(self):
        self.start = time.time()
        return None

    def __exit__(self, type, value, traceback):
        elapsed_time = time.time() - self.start
        print(self.message.format(elapsed_time))


# 1. Потоки.
def fetch_pic(num_pic):
    url = "https://picsum.photos/400/600"
    path = os.path.join(os.getcwd(), "img")
    for _ in range(num_pic):
        random_name = "".join(random.choices(string.ascii_letters + string.digits, k=5))
        response = requests.get(url)
        if response.status_code == 200:
            with open(f"{path}/{random_name}.jpg", "wb") as f:
                f.write(response.content)
                print(f"Fetched pic [{os.getpid()}]: {f.name}")


workers = 2
DATA_SIZE = 3

with timer("Elapsed time: {}s"):
    with ThreadPool(workers) as pool:
        input_data = [DATA_SIZE // workers for _ in range(workers)]
        pool.map(fetch_pic, input_data)

# 1 -  116.2
# 2 - 63.8
# 4 - 32.3
# 8 - 21.1
# 16 - 18.0
# 32 - 17.43
# 64 - 11.4
# 100 - 18
