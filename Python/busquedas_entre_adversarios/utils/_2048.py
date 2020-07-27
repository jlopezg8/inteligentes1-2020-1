"""Funciones de utilidad para el juego de 2048."""

import random

import matplotlib.pyplot as plt
import numpy as np


def _como_mutable(matriz):
    """Obtener una copia mutable de `matriz`."""
    return [list(fila) for fila in matriz]


def _como_hasheable(matriz):
    """Obtener una copia hasheable (y por tanto inmutable) de `matriz`."""
    return tuple(tuple(fila) for fila in matriz)


def _iter_matriz(matriz, con_indice=True):
    """
    Recorrer `matriz` en row-major order (de arriba a abajo de izquierda a
    derecha) generando tuplas de la forma (fila, columna, valor) si
    ``con_indice == True``, de lo contrario solo genera los valores.
    """
    for i, fila in enumerate(matriz):
        for j, val in enumerate(fila):
            yield (i, j, val) if con_indice else val


def jugar_maquina(estado):
    indices_0s = [(i, j) for i, j, val in _iter_matriz(estado) if val == 0]
    if indices_0s:
        estado = _como_mutable(estado)
        i, j = random.choice(indices_0s)
        estado[i][j] = 2
        return _como_hasheable(estado)
    else:
        return estado


def get_estado_inicial(n=4):
    estado = [[0] * n for _ in range(n)]
    return jugar_maquina(estado)


def get_utilidad(estado):
    return sum(1 for val in _iter_matriz(estado, con_indice=False) if val == 0)


def _mover_fila_hacia_izq(fila):
    no_0s = [e for e in fila if e != 0]  # juntar casillas sin combinarlas
    # Combinar las casillas juntas si tienen el mismo valor. La casilla
    # resultante no puede ser combinada con otra:
    combinadas = []
    i = 0
    while i < len(no_0s):
        if i + 1 < len(no_0s) and no_0s[i] == no_0s[i + 1]:
            combinadas.append(2 * no_0s[i])
            i += 1
        else:
            combinadas.append(no_0s[i])
        i += 1
    return combinadas + [0] * (len(fila) - len(combinadas))


DIRECCIONES = ('left', 'right', 'up', 'down')


def mover(estado, mov):
    if mov == 'left':
        estado = [_mover_fila_hacia_izq(fila) for fila in estado]
    elif mov == 'right':
        estado = [_mover_fila_hacia_izq(fila[::-1])[::-1] for fila in estado]
    elif mov == 'up':
        estado = [_mover_fila_hacia_izq(fila) for fila in np.rot90(estado)]
        estado = np.rot90(estado, -1)
    elif mov == 'down':
        estado = [_mover_fila_hacia_izq(fila) for fila in np.rot90(estado, -1)]
        estado = np.rot90(estado)
    else:
        raise ValueError(f'{mov=} no reconocido')
    return _como_hasheable(estado)


def gen_sucesores_jugador(estado):
    """Función generadora de los estados resultantes de aplicar las acciones
    del jugador a `estado`.
    """
    yield from (
        {mover(estado, direccion) for direccion in DIRECCIONES} - {estado})


def es_hoja(estado):
    return not list(gen_sucesores_jugador(estado))


JUGADOR = True


def get_sig_jugador(jugador):
    return not jugador


def gen_sucesores_maquina(estado):
    """Función generadora de los estados resultantes de aplicar las acciones
    de la máquina a `estado`.
    """
    indices_0s = [(i, j) for i, j, val in _iter_matriz(estado) if val == 0]
    if indices_0s:
        estado = _como_mutable(estado)
        for i, j in indices_0s:
            estado[i][j], val = 2, estado[i][j]
            yield _como_hasheable(estado)
            estado[i][j] = val
    else:  # a veces la máquina no puede colocar un 2, así que no hace nada
        yield estado


def gen_sucesores(estado, jugador):
    if jugador:
        yield from gen_sucesores_jugador(estado)
    else:
        yield from gen_sucesores_maquina(estado)


def _graficar_estado(estado):
    plt.cla()
    estado = np.array(estado)
    m, n = estado.shape
    mat = np.log2(estado, out=np.zeros_like(estado, dtype=float),
                  where=(estado > 0))
    plt.matshow(mat, fignum=0, cmap='YlOrRd', vmin=0, vmax=11,
                extent=(0, n, m, 0))
    plt.grid(True, color='black')
    plt.tick_params(direction='in', labeltop=False, labelleft=False)
    for i, j, val in _iter_matriz(estado):
        if val != 0:
            plt.text(x=j+.5, y=i+.5, s=val, size='xx-large', ha='center',
                     va='center')
    plt.pause(.1)


def graficar_estado(estado):
    _graficar_estado(estado)
    plt.show()


class ManejadorHumanoVsMaquina:
    def __init__(self, estado):
        self.estado = estado
        self.es_turno_jugador = True

    def __call__(self, evt):
        if self.es_turno_jugador and evt.key in DIRECCIONES:
            self._jugar_jugador(direccion=evt.key)

    def _jugar_jugador(self, direccion):
        self.es_turno_jugador = False
        jugada_jugador = mover(self.estado, direccion)
        if not np.array_equal(jugada_jugador, self.estado):
            self.estado = jugar_maquina(jugada_jugador)
            _graficar_estado(self.estado)
            if self._fin_juego():
                return
        self.es_turno_jugador = True

    def _fin_juego(self):
        if es_hoja(self.estado):
            plt.title(f'Fin del juego\nPuntaje={np.max(self.estado)}')
            plt.pause(.1)
            return True
        else:
            return False


def jugar_contra_maquina():
    estado = get_estado_inicial()
    mhvm = ManejadorHumanoVsMaquina(estado)
    plt.connect('key_press_event', mhvm)
    graficar_estado(estado)


if __name__ == "__main__":
    jugar_contra_maquina()
