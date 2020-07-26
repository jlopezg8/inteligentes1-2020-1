from contextlib import contextmanager
from time import time


@contextmanager
def cronometrar():
    inicio = time()
    yield
    print(f'Tiempo transcurrido: {time() - inicio}s')
