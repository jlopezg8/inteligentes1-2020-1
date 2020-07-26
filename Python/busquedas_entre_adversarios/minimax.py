"""Resolver un triqui usando el algoritmo minimax."""

class Minimax:
    def __init__(self, gen_sucesores, get_utilidad, get_sig_jugador):
        """
        Inicializa una instancia de Minimax para resolver un problema en
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

    def _minimax(self, estado, jugador_max, jugador):
        """Retorna la utilidad de un estado usando el algoritmo minimax.

        :param `estado`: estado actual del juego

        :param `jugador_max`: jugador MAX, las utilidades se calcularán desde
        su punto de vista

        :param `jugador`: jugador del turno actual
        """
        utilidad_estado = self.get_utilidad(estado, jugador_max)
        if utilidad_estado != 0:
            return utilidad_estado
        utilidades_sucesores = (
            self._minimax(sucesor, jugador_max, self.get_sig_jugador(jugador))
            for sucesor in self.gen_sucesores(estado, jugador))
        return (min, max)[jugador == jugador_max](
            utilidades_sucesores, default=utilidad_estado)

    def __call__(self, estado, jugador):
        """Asumiendo que `estado` corresponde a la última jugada de `jugador` y
        por lo tanto es el turno del oponente.
        """
        return self._minimax(estado, jugador, self.get_sig_jugador(jugador))

    def elegir_jugada(self, estado, jugador):
        """Retorna la mejor jugada para el estado y jugador actual."""
        return max(self.gen_sucesores(estado, jugador),
                   key=lambda sucesor: self(sucesor, jugador))


if __name__ == "__main__":
    import utils.triqui as triqui
    from utils import cronometrar

    args = triqui.parse_args()
    estado = triqui.ESTADO0
    jugador, maquina = triqui.O, triqui.X
    minimax = Minimax(triqui.gen_sucesores, triqui.get_utilidad,
                      triqui.get_sig_jugador)

    if args.entre_maquinas:  # máquina vs máquina
        while not triqui.es_hoja(estado):
            triqui._graficar_estado(estado)
            with cronometrar():
                print(f'{jugador=}')
                estado = minimax.elegir_jugada(estado, jugador)
            jugador = triqui.get_sig_jugador(jugador)
        triqui.graficar_estado(estado)
    else:  # humano vs máquina
        def elegir_jugada_maquina(estado):
            with cronometrar():
                return minimax.elegir_jugada(estado, maquina)
        triqui.jugar_contra_maquina(
            estado, jugador, elegir_jugada_maquina, args.inicia_maquina)
