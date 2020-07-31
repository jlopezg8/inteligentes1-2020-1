"""Funciones de utilidad para el juego de pente simplificado."""

import matplotlib.pyplot as plt
import numpy as np

from . import como_mutable
from .triqui import (
    O, X, _, gen_sucesores, get_sig_jugador, graficar_estado, _graficar_estado)


ESTADO_INICIAL = ((_,) * 6,) * 6


def es_hoja(estado):
    return not any(gen_sucesores(estado, O)) or get_utilidad(estado, O) != 0


def get_utilidad(estado, jugador):
    """Retorna 1 si el estado corresponde a una victoria para `jugador`, -1 si
    corresponde a una derrota para `jugador`, o 0 si corresponde a un empate o
    si ningún jugador ha ganado hasta el momento.
    """
    estado = np.array(estado)
    if _es_ganador(estado == jugador):
        return 1
    elif _es_ganador(estado == get_sig_jugador(jugador)):  # oponente
        return -1
    else:
        return 0


def _es_ganador(jugadas):
    return (any(jugadas[:-1].sum(axis=0) == 5)  # filas 0-4
            or any(jugadas[1:].sum(axis=0) == 5)  # filas 1-5
            or any(jugadas[:, :-1].sum(axis=1) == 5)  # columnas 0-4
            or any(jugadas[:, 1:].sum(axis=1) == 5)  # columnas 1-5
            or _gano_con_diag_principal(jugadas)  # diagonal principal
            or _gano_con_diag_principal(np.fliplr(jugadas)))  # diagonal sec


def _gano_con_diag_principal(jugadas):
    return (np.trace(jugadas[:-1]) == 5
            or np.trace(jugadas[:-1], offset=1) == 5
            or np.trace(jugadas[1:]) == 5
            or np.trace(jugadas[1:], offset=1) == 5)    


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
