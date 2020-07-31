"""Resolver un triqui usando la poda alfa-beta."""

from utils import mean


class PodaAlfaBeta:
    def __init__(self, es_hoja, get_utilidad, gen_sucesores, get_sig_jugador):
        """Inicializa una instancia de PodaAlfaBeta para resolver un problema
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
        self._funcs = (min, max)

    def __call__(
            self, estado, jugador_max, jugador, lim_profundidad=float('inf'),
            alfa=float('-inf'), beta=float('inf')):
        """Retorna la utilidad de un estado usando la poda alfa-beta.

        :param `estado`: estado actual del juego

        :param `jugador_max`: jugador MAX, las utilidades se calcularán desde
        su punto de vista

        :param `jugador`: jugador del turno actual

        :param `lim_profundidad`: profundidad a partir de la cual se corta la
        búsqueda
        """
        if lim_profundidad == 0 or self.es_hoja(estado):
            return self.get_utilidad(estado, jugador_max)

        utilidades_sucesores = (
            self(sucesor, jugador_max, self.get_sig_jugador(jugador),
                 lim_profundidad - 1, alfa, beta)
            for sucesor in self.gen_sucesores(estado, jugador))

        utilidades_consideradas = []
        if jugador == jugador_max:
            for utilidad_sucesor in utilidades_sucesores:
                utilidades_consideradas.append(utilidad_sucesor)
                if utilidad_sucesor >= beta:
                    break
                alfa = max(alfa, utilidad_sucesor)
        else:
            for utilidad_sucesor in utilidades_sucesores:
                utilidades_consideradas.append(utilidad_sucesor)
                if utilidad_sucesor <= alfa:
                    break
                beta = min(beta, utilidad_sucesor)
        return self._funcs[jugador == jugador_max](utilidades_consideradas)

    def elegir_jugada(self, estado, jugador, lim_profundidad=float('inf'),
                      con_barra_progreso=False):
        """Retorna la mejor jugada para el estado y jugador actual."""
        sucesores = self.gen_sucesores(estado, jugador)
        if con_barra_progreso:
            from tqdm import tqdm
            sucesores = tqdm(list(sucesores))
        return max(sucesores,
                   key=lambda sucesor: self(
                           sucesor, jugador, self.get_sig_jugador(jugador),
                           lim_profundidad))


class PodaAlfaBetaEstocastico(PodaAlfaBeta):
    def __init__(self, es_hoja, get_utilidad, gen_sucesores, get_sig_jugador):
        """Inicializa una instancia de PodaAlfaBetaEstocastico para resolver un
        problema concreto.

        :param `es_hoja`: función que recibe un estado y determina si es un
        nodo hoja

        :param `get_utilidad`: función que recibe un estado y un jugador y
        retorna la utilidad del estado desde el punto de vista del jugador

        :param `gen_sucesores`: función que recibe un estado y un jugador y
        genera los sucesores del estado desde el punto de vista del jugador

        :param `get_sig_jugador`: función que recibe el jugador del turno
        actual y retorna el jugador del turno siguiente
        """
        super().__init__(es_hoja, get_utilidad, gen_sucesores, get_sig_jugador)
        self._funcs = (mean, max)


if __name__ == "__main__":
    import utils.triqui as triqui
    from utils import cronometrar

    args = triqui.parse_args()
    poda_alfa_beta = PodaAlfaBeta(triqui.es_hoja, triqui.get_utilidad,
                                  triqui.gen_sucesores, triqui.get_sig_jugador)
    lim_profundidad = 5

    if args.entre_maquinas:
        def elegir_jugada(estado, jugador):
            with cronometrar():
                print(f'{jugador=}')
                return poda_alfa_beta.elegir_jugada(
                    estado, jugador, lim_profundidad)

        triqui.PartidaMaquinaVsMaquina(elegir_jugada)

    else:  # humano vs máquina
        def elegir_jugada(estado, jugador):
            with cronometrar():
                return poda_alfa_beta.elegir_jugada(
                    estado, jugador, lim_profundidad)

        triqui.PartidaHumanoVsMaquina(elegir_jugada, args.inicia_maquina)
