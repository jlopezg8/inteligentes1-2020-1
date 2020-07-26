"""Resolver un triqui usando la poda alfa-beta."""

class PodaAlfaBeta:
    def __init__(self, gen_sucesores, get_utilidad, get_sig_jugador):
        """
        Inicializa una instancia de PodaAlfaBeta para resolver un problema en
        concreto.

        :param `gen_sucesores`: función que recibe un estado y genera sus
        sucesores

        :param `get_utilidad`: función que recibe un estado y retorna su
        utilidad

        :param `get_sig_jugador`: función que recibe el jugador del turno
        actual y retorna el jugador del turno siguiente
        """
        self.gen_sucesores = gen_sucesores
        self.get_utilidad = get_utilidad
        self.get_sig_jugador = get_sig_jugador

    def _poda_alfa_beta(
            self, estado, jugador_max, jugador, lim_profundidad=float('inf'),
            alfa=float('-inf'), beta=float('inf')):
        """Retorna la utilidad de un estado usando el algoritmo minimax.

        :param `estado`: estado actual del juego

        :param `jugador_max`: jugador MAX, las utilidades se calcularán desde
        su punto de vista

        :param `jugador`: jugador del turno actual

        :param `lim_profundidad`: profundidad a partir de la cual se corta la
        búsqueda
        """
        if ((utilidad_estado := self.get_utilidad(estado, jugador_max)) != 0
            or lim_profundidad == 0
            or not (sucesores := list(self.gen_sucesores(estado, jugador)))):
            return utilidad_estado

        utilidades_sucesores = (
            self._poda_alfa_beta(
                sucesor, jugador_max, self.get_sig_jugador(jugador),
                lim_profundidad - 1, alfa, beta)
            for sucesor in sucesores)

        if jugador == jugador_max:
            utilidad = float('-inf')
            for utilidad_sucesor in utilidades_sucesores:
                utilidad = max(utilidad, utilidad_sucesor)
                alfa = max(alfa, utilidad)
                if alfa >= beta:
                    break
        else:
            utilidad = float('inf')
            for utilidad_sucesor in utilidades_sucesores:
                utilidad = min(utilidad, utilidad_sucesor)
                beta = min(beta, utilidad)
                if beta <= alfa:
                    break
        return utilidad

    def __call__(self, estado, jugador, lim_profundidad=float('inf')):
        """Asumiendo que `estado` corresponde a la última jugada de `jugador` y
        por lo tanto es el turno del oponente.
        """
        return self._poda_alfa_beta(
            estado, jugador, self.get_sig_jugador(jugador), lim_profundidad)

    def elegir_jugada(self, estado, jugador, lim_profundidad=float('inf')):
        """Retorna la mejor jugada para el estado y jugador actual."""
        return max(self.gen_sucesores(estado, jugador),
                   key=lambda sucesor: self(sucesor, jugador, lim_profundidad))


if __name__ == "__main__":
    import utils.triqui as triqui
    from utils import cronometrar

    args = triqui.parse_args()
    estado = triqui.ESTADO0
    jugador, maquina = triqui.O, triqui.X
    poda_alfa_beta = PodaAlfaBeta(
        triqui.gen_sucesores, triqui.get_utilidad, triqui.get_sig_jugador)
    lim_profundidad = 5

    if args.entre_maquinas:  # máquina vs máquina
        while not triqui.es_hoja(estado):
            triqui._graficar_estado(estado)
            with cronometrar():
                print(f'{jugador=}')
                estado = poda_alfa_beta.elegir_jugada(
                    estado, jugador, lim_profundidad)
            jugador = triqui.get_sig_jugador(jugador)
        triqui.graficar_estado(estado)
    else:  # humano vs máquina
        def elegir_jugada_maquina(estado):
            with cronometrar():
                return poda_alfa_beta.elegir_jugada(
                    estado, maquina, lim_profundidad)
        triqui.jugar_contra_maquina(
            estado, jugador, elegir_jugada_maquina, args.inicia_maquina)
