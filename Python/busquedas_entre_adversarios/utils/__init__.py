from contextlib import contextmanager
from time import time


def como_hasheable(matriz):
    """Obtener una copia hasheable (y por tanto inmutable) de `matriz`."""
    return tuple(tuple(fila) for fila in matriz)


def como_mutable(matriz):
    """Obtener una copia mutable de `matriz`."""
    return [list(fila) for fila in matriz]


def iter_matriz(matriz, con_indice=True):
    """
    Recorrer `matriz` en row-major order (de arriba a abajo de izquierda a
    derecha) generando tuplas de la forma (fila, columna, valor) si
    ``con_indice == True``, de lo contrario solo genera los valores.
    """
    for i, fila in enumerate(matriz):
        for j, val in enumerate(fila):
            yield (i, j, val) if con_indice else val


@contextmanager
def cronometrar():
    inicio = time()
    yield
    print(f'Tiempo transcurrido: {time() - inicio} s')


def mean(iterable, default=None):
    total = 0
    count = 0
    for e in iterable:
        total += e
        count += 1
    return total / count if count != 0 else default
