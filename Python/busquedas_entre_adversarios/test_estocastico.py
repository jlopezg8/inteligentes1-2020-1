"""Resolver una partida de 2048 usando el algoritmo minimax para juegos
estocásticos.
"""

import utils._2048 as _2048
from minimax import Minimax
from utils import cronometrar, mean

estado = _2048.get_estado_inicial()
minimax = Minimax(
    _2048.es_hoja, lambda estado, jugador: _2048.get_utilidad(estado),
    _2048.gen_sucesores, _2048.get_sig_jugador, funcs=(mean, max))

while not _2048.es_hoja(estado):
    _2048._graficar_estado(estado)
    with cronometrar():
        estado = minimax.elegir_jugada(estado, _2048.JUGADOR,
                                       lim_profundidad=5)
        estado = _2048.jugar_maquina(estado)
_2048.graficar_estado(estado)
