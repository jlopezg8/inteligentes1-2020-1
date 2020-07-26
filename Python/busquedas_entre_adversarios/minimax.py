"""Resolver un triqui usando el algoritmo minimax."""


class Minimax:
    def __init__(self, gen_sucesores, get_utilidad, get_sig_jugador,
                 funcs=(min, max)):
        """
        Inicializa una instancia de Minimax para resolver un problema en
        concreto.

        :param `gen_sucesores`: función que recibe un estado y genera sus
        sucesores

        :param `get_utilidad`: función que recibe un estado y retorna su
        utilidad

        :param `get_sig_jugador`: función que recibe el jugador del turno
        actual y retorna el jugador del turno siguiente

        :param `funcs`: dupla de funciones que reciben un iterable de
        utilidades y retornan la utilidad óptima; la función se elige de
        acuerdo al jugador del turno actual; también deben poder recibir un
        parámetro `default` que determina la utilidad a retornar si el iterable
        está vacío
        """
        self.gen_sucesores = gen_sucesores
        self.get_utilidad = get_utilidad
        self.get_sig_jugador = get_sig_jugador
        self.funcs = funcs

    def _minimax(self, estado, jugador_max, jugador, es_turno_func1):
        """Retorna la utilidad de un estado usando el algoritmo minimax.

        :param `estado`: estado actual del juego

        :param `jugador_max`: jugador MAX, las utilidades se calcularán desde
        su punto de vista

        :param `jugador`: jugador del turno actual

        :param `es_turno_func1`: si `jugador` es `self.funcs[1]`; ej: para
        ``self.funcs = (min, max)``, si `jugador` es MAX entonces
        `es_turno_func1=True`
        """
        utilidad_estado = self.get_utilidad(estado, jugador_max)
        if utilidad_estado != 0:
            return utilidad_estado
        utilidades_sucesores = (
            self._minimax(sucesor, jugador_max, self.get_sig_jugador(jugador),
                          es_turno_func1=not es_turno_func1)
            for sucesor in self.gen_sucesores(estado, jugador))
        return self.funcs[es_turno_func1](
            utilidades_sucesores, default=utilidad_estado)

    def __call__(self, estado, jugador):
        """Asumiendo que `estado` corresponde a la última jugada de `jugador` y
        por lo tanto es el turno del oponente.
        """
        return self._minimax(estado, jugador, self.get_sig_jugador(jugador),
                             es_turno_func1=False)

    def elegir_jugada(self, estado, jugador):
        """Retorna la mejor jugada para el estado y jugador actual."""
        return max(self.gen_sucesores(estado, jugador),
                   key=lambda sucesor: self(sucesor, jugador))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Jugar triqui.')
    parser.add_argument('-e', '--entre_maquinas', action='store_true',
                        help='juegan máquina vs máquina')
    parser.add_argument('-i', '--inicia_maquina', action='store_true',
                        help='inicia máquina (para humano vs máquina)')
    args = parser.parse_args()


    import matplotlib.pyplot as plt

    import utils.triqui as triqui
    from utils.indicadores_progreso import ContadorPasos


    estado = triqui.ESTADO0
    jugador, oponente = triqui.O, triqui.X
    minimax = Minimax(triqui.gen_sucesores, triqui.get_utilidad,
                      triqui.get_sig_jugador)


    def computador_vs_computador():
        global estado, jugador
        contador_pasos = ContadorPasos()
        while not triqui.es_hoja(estado):
            contador_pasos.send(f'{jugador=}'); next(contador_pasos)
            triqui._graficar_estado(estado); plt.pause(.1)
            estado = minimax.elegir_jugada(estado, jugador)
            jugador = triqui.get_sig_jugador(jugador)
        contador_pasos.close()
        triqui.graficar_estado(estado)


    def humano_vs_computador(inicia_computador):
        # TODO: implementar `inicia_computador`
        def elegir_jugada_oponente(estado):
            return minimax.elegir_jugada(estado, oponente)
        meh = triqui.ManejadorEleccionHumano(
            estado, jugador, elegir_jugada_oponente)
        plt.connect('button_press_event', meh)
        triqui.graficar_estado(estado)


    if args.entre_maquinas:
        computador_vs_computador()
    else:
        humano_vs_computador(args.inicia_maquina)