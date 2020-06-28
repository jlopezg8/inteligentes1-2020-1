"""Resolver un 8-puzzle usando búsqueda por anchura"""

from collections import deque

from utils.barras_progreso import contador_pasos


def buscar_por_anchura(estado0, gen_estados_alcanzables, es_estado_objetivo):
    """Retorna la ruta para resolver el problema, o `None` si no se encontró
    una solución.

    :param `estado0`: estado inicial
    :param `gen_estados_alcanzables` función que recibe un estado y genera los
        estados alcanzables a partir de este
    :param `es_estado_objetivo`: función que recibe un estado e indica si es el
        estado objetivo
    """
    frontera = deque([estado0])  # estados por visitar
    visitados = []
    padres = [None]  # ``padres[i]`` es el padre de ``visitados[i]``

    for pasos in contador_pasos():
        estado = frontera.popleft()
        visitados.append(estado)
        hijos = [hijo for hijo in gen_estados_alcanzables(estado)
                 if hijo not in visitados and hijo not in frontera]
        padres.extend([estado] * len(hijos))
        if any(es_estado_objetivo(objetivo := hijo) for hijo in hijos):
            break
        frontera.extend(hijos)
    else:
        return None  # No resuelto
    
    # Hallar la ruta partiendo del estado objetivo hasta llegar al estado inicial:
    # El último estado visitado corresponde al estado padre del estado objetivo:
    estado = visitados[-1]
    ruta = deque((estado, objetivo))
    while estado != estado0:
        estado = padres[visitados.index(estado)]
        ruta.appendleft(estado)
    return ruta


if __name__ == "__main__":
    import utils.eight_puzzle as ep

    X = ep.HUECO
    estado0 = (
        (5, 1, 2),
        (X, 7, 3),
        (6, 4, 8),
    )
    ep.graficar_estado(estado0)
    ruta = buscar_por_anchura(estado0, ep.gen_estados_alcanzables,
                              ep.es_estado_objetivo)
    ep.graficar_ruta(ruta)
