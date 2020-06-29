"""Resolver un 8-puzzle usando búsqueda voraz."""

from bisect import insort
from collections import deque, namedtuple

from utils.barras_progreso import ContadorPasos


_Nodo = namedtuple('Nodo', ['dist', 'estado', 'padre'])


def _reconstruir_ruta(nodo):
    ruta = deque([nodo.estado])
    while (nodo := nodo.padre) is not None:
        ruta.appendleft(nodo.estado)
    return ruta


def buscar_vorazmente(estado0, gen_estados_alcanzables, heuristica):
    """Retorna la ruta para resolver el problema, o `None` si no se encontró
    una solución.

    :param `estado0`: estado inicial
    :param `gen_estados_alcanzables` función que recibe un estado y genera los
        estados alcanzables a partir de este
    :param heuristica: función que recibe un estado y estima qué tan cerca está
        del estado objetivo; debe retornar 0 si el estado es el estado objetivo
    """
    contador_pasos = ContadorPasos()
    frontera = deque([_Nodo(estado=estado0, padre=None,
                            dist=heuristica(estado0))])
    considerados = {estado0}  # estados en la frontera o ya visitados
    while frontera:
        next(contador_pasos)
        nodo = frontera.popleft()
        if nodo.dist == 0:
            return _reconstruir_ruta(nodo)
        hijos = set(gen_estados_alcanzables(nodo.estado)) - considerados
        for hijo in hijos:
            considerados.add(hijo)
            insort(frontera, _Nodo(estado=hijo, padre=nodo,
                                   dist=heuristica(hijo)))
    return None  # no resuelto


if __name__ == "__main__":
    import utils.eight_puzzle as ep

    X = ep.HUECO
    estado0 = (
        (5, 1, 2),
        (X, 7, 3),
        (6, 4, 8),
    )
    ep.graficar_estado(estado0)
    ruta = buscar_vorazmente(estado0, ep.gen_estados_alcanzables,
                             heuristica=ep.dist_hamming)
    print(f'Solución de {len(ruta)} pasos')
    ep.graficar_ruta(ruta)
