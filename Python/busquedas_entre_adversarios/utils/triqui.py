"""Funciones de utilidad para el juego de triqui."""

import argparse
import random

import matplotlib.pyplot as plt
import numpy as np

from . import como_hasheable, como_mutable, iter_matriz


O = 'O'
X = 'X'
_ = '_'

ESTADO_INICIAL = (
    (_, _, _),
    (_, _, _),
    (_, _, _),
)


def es_hoja(estado):
    return not any(gen_sucesores(estado, O)) or get_utilidad(estado, O) != 0


def gen_sucesores(estado, jugador):
    """Función generadora de los estados sucesores de `estado`."""
    estado = como_mutable(estado)
    for i, j, val in iter_matriz(estado):
        if val == _:
            estado[i][j] = jugador
            yield como_hasheable(estado)
            estado[i][j] = _


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
            or np.trace(jugadas) == n  # diagonal principal
            or np.trace(np.fliplr(jugadas)) == n):  # diagonal secundaria
            return utilidad
    return 0


def graficar_estado(estado):
    _graficar_estado(estado)
    plt.show()


def _graficar_estado(estado):
    plt.grid(True, color='black')
    plt.ylim(len(estado), 0)
    plt.xlim(0, len(estado[0]))
    plt.yticks(range(1, len(estado)), labels=[])
    plt.xticks(range(1, len(estado[0])), labels=[])
    plt.gca().set_frame_on(False)
    for i, j, val in iter_matriz(estado):
        if val != _:
            plt.text(x=j+.5, y=i+.5, s=val, size=32, ha='center', va='center')
    plt.pause(.1)


def parse_args():
    parser = argparse.ArgumentParser(description='Jugar triqui.')
    parser.add_argument('-e', '--entre_maquinas', action='store_true',
                        help='juegan máquina vs máquina')
    parser.add_argument('-i', '--inicia_maquina', action='store_true',
                        help='inicia máquina (para humano vs máquina)')
    return parser.parse_args()


def PartidaMaquinaVsMaquina(elegir_jugada, maquina1=O,
                            estado_inicial=ESTADO_INICIAL):
    estado = estado_inicial
    jugador = maquina1
    while not es_hoja(estado):
        _graficar_estado(estado)
        estado = elegir_jugada(estado, jugador)
        jugador = get_sig_jugador(jugador)
    graficar_estado(estado)


class PartidaHumanoVsMaquina:
    def __init__(self, elegir_jugada, inicia_maquina=False, humano=O,
                 estado_inicial=ESTADO_INICIAL):
        self.elegir_jugada = elegir_jugada
        self.estado = como_mutable(estado_inicial)
        self.humano = humano
        self.maquina = get_sig_jugador(humano)
        self._iniciar(inicia_maquina)

    def _iniciar(self, inicia_maquina):
        _graficar_estado(self.estado)
        if inicia_maquina:
            self._jugar_maquina()
        self.es_turno_humano = True
        plt.connect('button_press_event', self)
        plt.show()

    def __call__(self, evt):
        if self.es_turno_humano and evt.inaxes:
            self.es_turno_humano = False
            i, j = int(evt.ydata), int(evt.xdata)
            if self._jugar_jugador(i, j):
                self._jugar_maquina()
            self.es_turno_humano = True

    def _jugar_jugador(self, i, j):
        if self.estado[i][j] == _ and not es_hoja(self.estado):
            self.estado[i][j] = self.humano
            _graficar_estado(self.estado)
            return True
        else:
            return False

    def _jugar_maquina(self):
        if not es_hoja(self.estado):
            self.estado = como_mutable(
                self.elegir_jugada(self.estado, self.maquina))
            _graficar_estado(self.estado)
