"""This is just a simple example for testing cprofilev. To see cprofilev in
action, run

python -m cprofilev example_for_profiling.py
"""

import random
import time


def product(x, y):
    return x * y


def main():
    x = 1.
    while True:
        x = product(x, 0.5 + random.random())
        time.sleep(0.1)


if __name__ == '__main__':
    main()
