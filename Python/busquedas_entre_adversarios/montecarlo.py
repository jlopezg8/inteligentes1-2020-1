"""Resolver una partida de 2048 usando simulación Montecarlo."""

import random
import sys

from utils import mean


class Montecarlo:
    def __init__(self, es_hoja, get_utilidad, gen_sucesores, get_sig_jugador):
        """Inicializa una instancia de Montecarlo para resolver un problema
        concreto.

        :param `es_hoja`: función que recibe un estado y determina si es un
        nodo hoja

        :param `get_utilidad`: función que recibe un estado y un jugador y
        retorna la utilidad del estado desde el punto de vista del jugador

        :param `gen_sucesores`: función que recibe un estado y un jugador y
        genera los sucesores del estado desde el punto de vista del jugador

        :param `get_sig_jugador`: función que recibe el jugador del turno
        actual y retorna el jugador del turno siguiente
        """
        self.es_hoja = es_hoja
        self.get_utilidad = get_utilidad
        self.gen_sucesores = gen_sucesores
        self.get_sig_jugador = get_sig_jugador

    def __call__(self, estado, jugador_max, jugador, n_sims,
                 lim_profundidad=float('inf')):
        """Retorna la utilidad de un estado usando la simulación Montecarlo.

        :param `estado`: estado actual del juego

        :param `jugador_max`: jugador MAX, las utilidades se calcularán desde
        su punto de vista

        :param `jugador`: jugador del turno actual

        :param `n_sims`: número de partidas del juego simuladas

        :param `lim_profundidad`: profundidad a partir de la cual se detienen
        las simulaciones si aún no han llegado a un nodo hoja; por defecto no
        hay límite
        """
        return mean(
            self._eval_sim(estado, jugador_max, jugador, lim_profundidad)
            for _ in range(n_sims))

    def _eval_sim(self, estado, jugador_max, jugador,
                  lim_profundidad=float('inf')):
        while lim_profundidad > 0 and not self.es_hoja(estado):
            sucesores = list(self.gen_sucesores(estado, jugador))
            estado = random.choice(sucesores)
            jugador = self.get_sig_jugador(jugador)
            lim_profundidad -= 1
        return self.get_utilidad(estado, jugador_max)

    def elegir_jugada(
            self, estado, jugador, n_sims, lim_profundidad=float('inf'),
            con_barra_progreso=False):
        """Retorna la mejor jugada para el estado y jugador actual."""
        sucesores = self.gen_sucesores(estado, jugador)
        if con_barra_progreso:
            from tqdm import tqdm
            sucesores = tqdm(list(sucesores))
        return max(sucesores,
                   key=lambda sucesor: self(
                           sucesor, jugador, self.get_sig_jugador(jugador),
                           n_sims, lim_profundidad))


if __name__ == "__main__":
    import utils._2048 as _2048
    from utils import cronometrar

    montecarlo = Montecarlo(
        _2048.es_hoja, lambda estado, jugador: _2048.get_utilidad(estado),
        _2048.gen_sucesores, _2048.get_sig_jugador)

    def elegir_jugada(estado, jugador):
        #with cronometrar():
        return montecarlo.elegir_jugada(estado, jugador, n_sims=15,
                                        lim_profundidad=10)

    _2048.PartidaMaquinaVsMaquina(elegir_jugada)
