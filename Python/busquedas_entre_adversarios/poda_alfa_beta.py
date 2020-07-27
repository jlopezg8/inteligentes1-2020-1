"""Resolver un triqui usando la poda alfa-beta."""

class PodaAlfaBeta:
    def __init__(self, es_hoja, get_utilidad, gen_sucesores, get_sig_jugador,
                 funcs=(min, max)):
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

        :param `funcs`: dupla de funciones que reciben un iterable de
        utilidades y seleccionan la utilidad óptima desde el punto de vista del
        jugador del turno actual. Por defecto ``funcs=(min, max)``, así el
        jugador MIN usa `funcs[0]` y el jugador MAX usa `funcs[1]`. Es común
        reemplazar `min` por `utils.mean` para juegos estocásticos.
        """        
        self.es_hoja = es_hoja
        self.get_utilidad = get_utilidad
        self.gen_sucesores = gen_sucesores
        self.get_sig_jugador = get_sig_jugador
        self.funcs = funcs

    def __call__(
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
        if lim_profundidad == 0 or self.es_hoja(estado):
            return self.get_utilidad(estado, jugador_max)

        utilidades_sucesores = (
            self(sucesor, jugador_max, self.get_sig_jugador(jugador),
                 lim_profundidad - 1, alfa, beta)
            for sucesor in self.gen_sucesores(estado, jugador))

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

    def elegir_jugada(self, estado, jugador, lim_profundidad=float('inf')):
        """Retorna la mejor jugada para el estado y jugador actual."""
        return max(
            self.gen_sucesores(estado, jugador),
            key=lambda sucesor: self(
                sucesor, jugador, self.get_sig_jugador(jugador),
                lim_profundidad))


if __name__ == "__main__":
    import utils.triqui as triqui
    from utils import cronometrar

    args = triqui.parse_args()
    estado = triqui.ESTADO0
    jugador, maquina = triqui.O, triqui.X
    poda_alfa_beta = PodaAlfaBeta(triqui.es_hoja, triqui.get_utilidad,
                                  triqui.gen_sucesores, triqui.get_sig_jugador)
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
