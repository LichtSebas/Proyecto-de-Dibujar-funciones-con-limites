import numpy as np
import math
from scipy.integrate import simpson, trapezoid

class SistemaFunciones:

    def __init__(self, x_min=-10, x_max=10, y_min=-10, y_max=10):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max

        # Lista → (func_callable, texto, xmin, xmax)
        self.funciones = []

    # --------------------------------------------------------
    # Establecer límites del plano
    # --------------------------------------------------------
    def configurar_plano(self, x_min, x_max, y_min, y_max):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max

    # --------------------------------------------------------
    # Simpson 1/3
    # --------------------------------------------------------
    def area_simpson(self, func_texto, a, b, n=1000):
        # Buscar función lambda asociada al texto
        for func, txt, xmin, xmax in self.funciones:
            if txt == func_texto:
                f = func
                break
        else:
            raise ValueError("Función no encontrada")

        xs = np.linspace(a, b, n + 1)
        ys = f(xs)

        if ys is None or np.any(np.isnan(ys)):
            raise ValueError("La función no se pudo evaluar.")

        return simpson(ys, xs)

    # --------------------------------------------------------
    # Trapecios
    # --------------------------------------------------------
    def area_trapecios(self, func_texto, a, b, n=1000):
        for func, txt, xmin, xmax in self.funciones:
            if txt == func_texto:
                f = func
                break
        else:
            raise ValueError("Función no encontrada")

        xs = np.linspace(a, b, n + 1)
        ys = f(xs)

        if ys is None or np.any(np.isnan(ys)):
            raise ValueError("La función no se pudo evaluar.")

        return trapezoid(ys, xs)

    # --------------------------------------------------------
    # Sólido de revolución
    # --------------------------------------------------------
    def solido_revolucion(self, func_texto, a, b, n=1000):
        for func, txt, xmin, xmax in self.funciones:
            if txt == func_texto:
                f = func
                break
        else:
            raise ValueError("Función no encontrada")

        xs = np.linspace(a, b, n + 1)
        ys = f(xs)

        if ys is None or np.any(np.isnan(ys)):
            raise ValueError("La función no se pudo evaluar.")

        return np.pi * simpson(ys**2, xs)
