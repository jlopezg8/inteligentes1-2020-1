"""Funciones de utilidad para el juego de triqui"""

import matplotlib.pyplot as plt
import numpy as np


O = 'O'
X = 'X'
_ = '_'

ESTADO0 = (
    (_, _, _),
    (_, _, _),
    (_, _, _),
)


def get_sig_jugador(jugador):
    """Retorna el jugador del turno siguiente, donde `jugador` es el jugador
    del turno actual.
    """
    return O if jugador == X else X


def get_utilidad(estado, jugador):
    """Retorna 1 si el estado corresponde a una victoria para `jugador`, -1 si
    corresponde a una derrota para `jugador`, o 0 si corresponde a un empate o
    si ningún jugador ha ganado hasta el momento.
    """
    estado = np.array(estado)
    m, n = estado.shape  # asumir que m == n (estado es una matriz cuadrada)
    jugadores = (
        (estado == jugador, 1),  # jugador
        ((estado == get_sig_jugador(jugador)), -1),  # oponente
    )
    for jugadas, utilidad in jugadores:
        if (any(jugadas.sum(axis=0) == m)  # columnas
            or any(jugadas.sum(axis=1) == n)  # filas
            or np.trace(jugadas).sum() == n  # diagonal principal
            or np.trace(np.fliplr(jugadas)) == n):  # diagonal secundaria

            return utilidad
    return 0


def _como_hasheable(matriz):
    """Retorna una copia hasheable (y por tanto inmutable) de `matriz`."""
    return tuple(tuple(fila) for fila in matriz)


def _como_mutable(matriz):
    """Retorna una copia mutable de `matriz`."""
    return [list(fila) for fila in matriz]


def _iter_matriz(matriz, con_indice=True):
    """
    Recorre `matriz` en row-major order (de arriba a abajo de izquierda a
    derecha) generando tuplas de la forma (fila, columna, valor) si
    ``con_indice == True``, de lo contrario solo genera los valores.
    """
    for i, fila in enumerate(matriz):
        for j, val in enumerate(fila):
            yield (i, j, val) if con_indice else val


def gen_sucesores(estado, jugador):
    """Función generadora de los estados sucesores de `estado`."""
    estado = _como_mutable(estado)
    for i, j, val in _iter_matriz(estado):
        if val == _:
            estado[i][j] = jugador
            yield _como_hasheable(estado)
            estado[i][j] = _


def es_hoja(estado):
    return not list(gen_sucesores(estado, O)) or get_utilidad(estado, O) != 0


def _graficar_estado(estado):
    plt.grid(True, color='black')
    plt.ylim(len(estado), 0)
    plt.xlim(0, len(estado[0]))
    plt.yticks(range(1, len(estado)), labels=[])
    plt.xticks(range(1, len(estado[0])), labels=[])
    plt.gca().set_frame_on(False)
    for i, j, val in _iter_matriz(estado):
        if val != _:
            plt.text(x=j+.5, y=i+.5, s=val, size=32, ha='center', va='center')


def graficar_estado(estado):
    _graficar_estado(estado)
    plt.show()


def graficar_estados(estados, intervalo_s=1):
    for estado in estados:
        plt.cla()
        _graficar_estado(estado)
        plt.pause(intervalo_s)
    plt.show()


class ManejadorEleccionHumano:
    def __init__(self, estado, jugador, elegir_jugada_oponente):
        self.es_turno_jugador = True
        self.estado = _como_mutable(estado)
        self.jugador = jugador
        self.elegir_jugada_oponente = elegir_jugada_oponente

    def __call__(self, evt):
        if self.es_turno_jugador and evt.inaxes:
            self.es_turno_jugador = False
            if self._jugar_jugador(i=int(evt.ydata), j=int(evt.xdata)):
                self._jugar_oponente()
            self.es_turno_jugador = True
    
    def _jugar_jugador(self, i, j):
        if self.estado[i][j] == _ and not es_hoja(self.estado):
            self.estado[i][j] = self.jugador
            _graficar_estado(self.estado); plt.pause(.1)
            return True
        else:
            return False
    
    def _jugar_oponente(self):
        if not es_hoja(self.estado):
            self.estado = _como_mutable(
                self.elegir_jugada_oponente(self.estado))
            _graficar_estado(self.estado); plt.pause(.1)
