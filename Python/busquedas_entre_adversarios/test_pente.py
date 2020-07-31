"""Resolver una partida de pente simplificado usando la poda alfa-beta."""

import utils.pente as pente
from poda_alfa_beta import PodaAlfaBeta
from utils import cronometrar, como_mutable

poda_alfa_beta = PodaAlfaBeta(pente.es_hoja, pente.get_utilidad,
                              pente.gen_sucesores, pente.get_sig_jugador)

def elegir_jugada(estado, jugador):
    with cronometrar():
        return poda_alfa_beta.elegir_jugada(
            estado, jugador, lim_profundidad=4, con_barra_progreso=True)

pente.PartidaHumanoVsMaquina(elegir_jugada, inicia_maquina=True)
