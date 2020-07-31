"""Resolver un triqui usando el algoritmo minimax."""

from utils import mean


class Minimax:
    def __init__(self, es_hoja, get_utilidad, gen_sucesores, get_sig_jugador):
        """Inicializa una instancia de Minimax para resolver un problema
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

    def __call__(self, estado, jugador_max, jugador,
                 lim_profundidad=float('inf')):
        """Retorna la utilidad de un estado usando el algoritmo minimax.

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
                 lim_profundidad - 1)
            for sucesor in self.gen_sucesores(estado, jugador))
        return self._funcs[jugador == jugador_max](utilidades_sucesores)

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


class Expectimax(Minimax):
    def __init__(self, es_hoja, get_utilidad, gen_sucesores, get_sig_jugador):
        """Inicializa una instancia de Expectimax para resolver un problema
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
        super().__init__(es_hoja, get_utilidad, gen_sucesores, get_sig_jugador)
        self._funcs = (mean, max)


if __name__ == "__main__":
    import utils.triqui as triqui
    from utils import cronometrar

    args = triqui.parse_args()
    minimax = Minimax(triqui.es_hoja, triqui.get_utilidad,
                      triqui.gen_sucesores, triqui.get_sig_jugador)

    if args.entre_maquinas:
        def elegir_jugada(estado, jugador):
            with cronometrar():
                print(f'{jugador=}')
                return minimax.elegir_jugada(estado, jugador)

        triqui.PartidaMaquinaVsMaquina(elegir_jugada)

    else:  # humano vs máquina
        def elegir_jugada(estado, jugador):
            with cronometrar():
                return minimax.elegir_jugada(estado, jugador)

        triqui.PartidaHumanoVsMaquina(elegir_jugada, args.inicia_maquina)
