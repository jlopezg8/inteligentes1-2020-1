"""Objetos para visualizar el progreso de un algoritmo."""

from itertools import count


def contador_pasos_simple():
    """Imprime el número de pasos en líneas separadas."""
    for paso in count(start=1):
        print(paso)
        yield paso


def contador_pasos_elaborado():
    """Imprime el número de pasos en una barra de progreso.
    
    Requiere `tqdm`.
    """
    from tqdm import tqdm
    # `tqdm` no funciona correctamente con `itertools`:
    #return tqdm(count(start=1))
    t = tqdm()
    for paso in count(start=1):
        t.update()
        yield paso


def contador_pasos():
    """Crea un iterador que imprime y retorna el número de pasos que lleva un
    algoritmo en cada iteración.
    """
    try:
        return contador_pasos_elaborado()
    except ImportError:
        return contador_pasos_simple()
