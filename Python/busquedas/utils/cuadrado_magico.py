"""Estructuras de datos y funciones útiles para resolver el problema del
cuadrado mágico.
"""

import numpy as np


def gen_sucesores(estado):
    estado = np.asarray(estado)
    num = 1 + max((estado[i, j] for i, j in np.argwhere(estado != 0)),
                  default=0)
    for i, j in np.argwhere(estado == 0):
        estado[i, j] = num
        yield tuple(tuple(fila) for fila in estado)
        estado[i, j] = 0


def test_objetivo(estado):
    estado = np.asarray(estado)
    suma_diag1 = estado[0, 0] + estado[1, 1] + estado[2, 2]
    suma_diag2 = estado[0, 2] + estado[1, 1] + estado[2, 0]
    sumas_cols = estado.sum(axis=0)
    sumas_filas = estado.sum(axis=1)
    return (suma_diag1 == suma_diag2 == sumas_cols[0] == sumas_filas[0]
            and all(suma_col == suma_diag1 for suma_col in sumas_cols)
            and all(suma_fila == suma_diag1 for suma_fila in sumas_filas))


def heuristica(estado, c1=145, c2=145, c3=1):
    estado = np.asarray(estado)
    suma_diag1 = estado[0, 0] + estado[1, 1] + estado[2, 2]
    suma_diag2 = estado[0, 2] + estado[1, 1] + estado[2, 0]
    sumas = np.concatenate(
        ([suma_diag1, suma_diag2], estado.sum(axis=0), estado.sum(axis=1)))
    return (c1 * (estado[0, 0] != 4) + c2 * np.count_nonzero(estado == 0)
            + c3 * np.var(sumas))
