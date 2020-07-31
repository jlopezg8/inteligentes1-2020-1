"""Resolver una partida de 2048 usando un algoritmo de búsqueda para juegos
estocásticos.
"""

import utils._2048 as _2048
from poda_alfa_beta import PodaAlfaBetaEstocastico as Algoritmo
from utils import cronometrar

algoritmo = Algoritmo(
    _2048.es_hoja, lambda estado, jugador: _2048.get_utilidad(estado),
    _2048.gen_sucesores, _2048.get_sig_jugador)

def elegir_jugada(estado, jugador):
    with cronometrar():
        return algoritmo.elegir_jugada(estado, jugador, lim_profundidad=4)

_2048.PartidaMaquinaVsMaquina(elegir_jugada)
