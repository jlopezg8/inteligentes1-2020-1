from contextlib import contextmanager
from time import time


@contextmanager
def cronometrar():
    inicio = time()
    yield
    print(f'Tiempo transcurrido: {time() - inicio}s')


def mean(iterable, default=None):
    total = 0
    count = 0
    for e in iterable:
        total += e
        count += 1
    return default if count == 0 else total / count
