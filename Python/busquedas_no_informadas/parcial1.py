#%% Preparación del punto 2 y 3:
import utils.problema_jarras as pj
estado0 = (pj.Jarra(12), pj.Jarra(8), pj.Jarra(3))
test_objetivo = pj.crear_test_objetivo(objetivo=1)


#%% Punto 2
from anchura import buscar_en_anchura
ruta = buscar_en_anchura(estado0, pj.gen_sucesores, test_objetivo)


#%% Punto 3
from profundidad import buscar_en_profundidad_iterativa
ruta = buscar_en_profundidad_iterativa(
    estado0, pj.gen_sucesores, test_objetivo)


#%% Preparación del punto 5:
import utils.cuadrado_magico as cm


#%% Punto 5 con búsqueda en profundidad:
from profundidad import buscar_en_profundidad_limitada
ruta = buscar_en_profundidad_limitada(
    cm.ESTADO0, cm.gen_sucesores, cm.test_objetivo, max_profundidad=9)
print(ruta[-1] if ruta else 'solución no encontrada')


#%% Punto 5 con búsqueda A*:
from a_estrella import buscar_con_a_estrella
ruta = buscar_con_a_estrella(cm.ESTADO0, cm.gen_sucesores, cm.heuristica)
print(ruta[-1] if ruta else 'solución no encontrada')