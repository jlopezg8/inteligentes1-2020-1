"""Soluciones numéricas a problemas de cinemática inversa con seis grados de
libertad usando optimización por enjambre de partículas.
"""

from collections import namedtuple
from math import cos, pi, sin, sqrt

import numpy as np
import pyswarms as ps

try:
    from math import dist as dist_euclidiana  # Python 3.8+
except ImportError:
    def dist_euclidiana(p, q):
        return sqrt(sum((px - qx) ** 2.0 for px, qx in zip(p, q)))


def hallar_matriz_transformacion_articulacion(theta, alfa, d, a):
    return np.array([
        [cos(theta), -sin(theta)*cos(alfa),  sin(theta)*sin(alfa), a*cos(theta)],
        [sin(theta),  cos(theta)*cos(alfa), -cos(theta)*sin(alfa), a*sin(theta)],
        [         0,             sin(alfa),             cos(alfa),            d],
        [         0,                     0,                     0,            1]])


d1 = d2 = d4 = d5 = d6 = 3  # longitudes de las articulaciones rotatorias


def hallar_pos_punta(vars_articulaciones):
    theta1, theta2, d3, theta4, theta5, theta6 = vars_articulaciones

    # Matrices de transformación para cada articulación:
    t_00 = np.identity(4)
    t_01 = hallar_matriz_transformacion_articulacion(theta1 , alfa=-pi/2, d=d2, a=0)
    t_12 = hallar_matriz_transformacion_articulacion(theta2 , alfa=-pi/2, d=d2, a=0)
    t_23 = hallar_matriz_transformacion_articulacion(theta=0, alfa=-pi/2, d=d3, a=0)
    t_34 = hallar_matriz_transformacion_articulacion(theta4 , alfa=-pi/2, d=d4, a=0)
    t_45 = hallar_matriz_transformacion_articulacion(theta5 , alfa=pi/2 , d=0 , a=0)
    t_56 = hallar_matriz_transformacion_articulacion(theta6 , alfa=0    , d=d6, a=0)

    # Multiplicación de matrices:
    matriz_transformacion = t_00 @ t_01 @ t_12 @ t_23 @ t_34 @ t_45 @ t_56

    # Las coordenadas de la punta se encuentran en los 3 primeros elementos de
    # la columna 4 (o 3 empezando desde 0):
    return matriz_transformacion[:3, 3]


def crear_func_obj(obj):
    def func_obj(enjambre):
        return np.array([
            dist_euclidiana(hallar_pos_punta(vars_articulaciones=particula),
                            obj)
            for particula in enjambre])

    return func_obj


restricciones = (
    #          t1    t2   d3  t4      t5     t6
    np.array([-pi, -pi/2, 1, -pi, -5*pi/36, -pi]),  # inf
    np.array([ pi,  pi/2, 3,  pi,  5*pi/36,  pi]))  # sup

func_obj = crear_func_obj(obj=(-2, 2, 3))

Punto = namedtuple('Punto', ['x', 'y', 'z'])
VarsArticulaciones = namedtuple(
    'VarsArticulaciones',
    ['theta1', 'theta2', 'd3', 'theta4', 'theta5', 'theta6'])


def probar_params(param_cognitivo, param_social, param_inercia):
    params = {
        'c1': param_cognitivo,
        'c2': param_social,
        'w': param_inercia,
    }
    optimizador = ps.single.GlobalBestPSO(
        n_particles=20, dimensions=6, options=params, bounds=restricciones)
    mejor_costo, vars_articulaciones = optimizador.optimize(
        func_obj, iters=1000)

    print(VarsArticulaciones._make(vars_articulaciones))
    print(f'=> {Punto._make(hallar_pos_punta(vars_articulaciones))} '
          f'(dist={mejor_costo})')


probar_params(param_cognitivo=1.5, param_social=1.5, param_inercia=0.5)
