"""Resolver un 8-puzzle usando búsqueda por anchura"""

from collections import deque
from contextlib import closing, suppress
from itertools import count

import numpy as np

try:
    from tqdm import tqdm
except ImportError:  # en caso de que `tqdm` no esté instalado:
    def tqdm(it, *args, **kwargs):
        for e in it:
            print(e)
            yield e

    tqdm.close = lambda: None

from eight_puzzle import *


estado0 = (
    (5, 1, 2),
    (X, 7, 3),
    (6, 4, 8),
)
#graficar_estado(estado0)

#resuelto = False
frontera = deque([estado0])  # estados por visitar
visitados = []
padres = [None]  # ``padres[i]`` es el padre de ``visitados[i]``

#with closing(iter(tqdm(count(start=1)))) as barra_progreso:  # ignore eso
with closing(tqdm(count(start=1))) as barra_progreso:  # ignore eso
    #while not resuelto:
    for pasos in barra_progreso:
        #pasos = next(barra_progreso)
        estado = frontera.popleft()
        visitados.append(estado)
        hijos = set(gen_estados_alcanzables(estado))
        hijos.difference_update(visitados, frontera)
        padres.extend((estado,) * len(hijos))
        """
        for hijo in hijos:
            if es_objetivo(hijo):
                objetivo = hijo
                resuelto = True
                break
        else:
            frontera.extend(hijos)
        """
        with suppress(StopIteration):
            objetivo = next(hijo for hijo in hijos if es_objetivo(hijo))
            break
        frontera.extend(hijos)


# Hallar la ruta partiendo del estado objetivo hasta llegar al estado inicial:
# El último estado visitado corresponde al estado padre del estado objetivo:
estado = visitados[-1]
ruta = deque((estado, objetivo))
while estado != estado0:
    estado = padres[visitados.index(estado)]
    ruta.appendleft(estado)


graficar_ruta(ruta)
