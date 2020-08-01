"""Funciones de utilidad para el juego de 2048.

Para jugar una partida ejecutar el script desde el directorio padre como
``py -m utils._2048``.
"""

import random
from math import log2

import matplotlib.pyplot as plt
import numpy as np

from . import como_hasheable, como_mutable, iter_matriz


def es_hoja(estado):
    return not any(_gen_sucesores_jugador(estado))


def gen_estado_inicial(n=4):
    estado = np.zeros((n, n), dtype=int)
    return jugar_maquina(estado)


def gen_sucesores(estado, jugador):
    if jugador:
        yield from _gen_sucesores_jugador(estado)
    else:
        yield from _gen_sucesores_maquina(estado)


# Por el orden de esta lista se favorecen los movimientos hacia arriba y hacia
# la izquierda:
DIRECCIONES = ('up', 'left', 'down', 'right')


def _gen_sucesores_jugador(estado):
    """Función generadora de los estados resultantes de aplicar las acciones
    del jugador a `estado`.
    """
    visitados = {estado}
    for direccion in DIRECCIONES:
        if (sucesor := mover(estado, direccion)) not in visitados:
            yield sucesor
            visitados.add(sucesor)


def _gen_sucesores_maquina(estado):
    """Función generadora de los estados resultantes de aplicar las acciones
    de la máquina a `estado`.
    """
    indices_0s = [(i, j) for i, j, val in iter_matriz(estado) if val == 0]
    if indices_0s:
        estado = como_mutable(estado)
        for i, j in indices_0s:
            estado[i][j] = 2
            yield como_hasheable(estado)
            estado[i][j] = 0
    else:  # a veces la máquina no puede colocar un 2, así que no hace nada
        yield estado


def get_puntaje(estado):
    return np.max(estado)


JUGADOR = True


def get_sig_jugador(jugador):
    return not jugador


def get_utilidad(estado, p_vacias=1, p_puntaje=1, p_monotonia=1):
    estado = np.array(estado)
    n_vacias = np.count_nonzero(estado == 0)
    lg_puntaje = log2(estado.max())
    monotonia = _get_monotonia(estado)
    return p_vacias*n_vacias + p_puntaje*lg_puntaje + p_monotonia*monotonia


def _get_esquinidad(estado):
    """
    - Récord: 2048>512
    - Corre muy rápido: (13.8 us +- 613 ns) / estado
    - Favorece la esquina superior izquierda
    """
    esquinidad = 0
    m, n = estado.shape
    for i in range(m):
        for j in range(n - 1):
            if estado[i, j] < estado[i, j + 1]:
                break
            esquinidad += 1
    for j in range(n):
        for i in range(m - 1):
            if estado[i, j] < estado[i + 1, j]:
                break
            esquinidad += 1
    return esquinidad


def _get_monotonia(estado):
    """
    - Récord: 4096>1024
    - Corre más o menos rápido: (73.2 us +- 1.18 us) / estado
    - Suele mover la casilla de mayor valor alrededor del tablero
    """
    lgs = np.log2(estado, out=np.zeros_like(estado, dtype=float),
                  where=estado>0)
    difs_contiguos_col = lgs[:-1] - lgs[1:]
    monotonia_vertical = max(
        difs_contiguos_col.sum(where=difs_contiguos_col>0),
        -difs_contiguos_col.sum(where=difs_contiguos_col<0))
    difs_contiguos_fila = lgs[:, :-1] - lgs[:, 1:]
    monotonia_horizontal = max(
        difs_contiguos_fila.sum(where=difs_contiguos_fila>0),
        -difs_contiguos_fila.sum(where=difs_contiguos_fila<0))
    return .5 * (monotonia_vertical + monotonia_horizontal) / lgs.max()


def graficar_estado(estado):
    _graficar_estado(estado)
    plt.show()


def _graficar_estado(estado):
    plt.cla()
    estado = np.array(estado)
    m, n = estado.shape
    mat = np.log2(estado, out=np.zeros_like(estado, dtype=float),
                  where=estado>0)
    plt.matshow(mat, fignum=0, cmap='YlOrRd', vmin=0, vmax=11,
                extent=(0, n, m, 0))
    plt.grid(True, color='black')
    plt.tick_params(direction='in', labeltop=False, labelleft=False)
    for i, j, val in iter_matriz(estado):
        if val != 0:
            plt.text(x=j+.5, y=i+.5, s=val, size='xx-large', ha='center',
                     va='center')
    plt.pause(.001)


def jugar_maquina(estado):
    indices_0s = [(i, j) for i, j, val in iter_matriz(estado) if val == 0]
    if indices_0s:
        estado = como_mutable(estado)
        i, j = random.choice(indices_0s)
        estado[i][j] = 2
        return como_hasheable(estado)
    else:
        return estado


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
    return como_hasheable(estado)


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


def PartidaMaquinaVsMaquina(elegir_jugada):
    estado = gen_estado_inicial()
    while not es_hoja(estado):
        _graficar_estado(estado)
        estado = elegir_jugada(estado, JUGADOR)
        estado = jugar_maquina(estado)
    graficar_estado(estado)


class PartidaHumanoVsMaquina:
    def __init__(self):
        self.estado = gen_estado_inicial()
        self.es_turno_jugador = True
        self._iniciar()

    def _iniciar(self):
        plt.connect('key_press_event', self)
        graficar_estado(self.estado)

    def __call__(self, evt):
        if self.es_turno_jugador and evt.key in DIRECCIONES:
            self._jugar_jugador(direccion=evt.key)

    def _jugar_jugador(self, direccion):
        self.es_turno_jugador = False
        jugada_jugador = mover(self.estado, direccion)
        if jugada_jugador != self.estado:
            self.estado = jugar_maquina(jugada_jugador)
            _graficar_estado(self.estado)
            if self.fin_juego():
                return
        self.es_turno_jugador = True

    def fin_juego(self):
        if es_hoja(self.estado):
            plt.title(f'Fin del juego\nPuntaje={get_puntaje(self.estado)}')
            plt.pause(.001)
            return True
        else:
            return False


if __name__ == "__main__":
    PartidaHumanoVsMaquina()
