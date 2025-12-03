import numpy as np
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg


class PlotWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.fig = Figure(figsize=(5, 4))
        self.canvas = FigureCanvasQTAgg(self.fig)

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    # -------------------------------------------------------
    # DIBUJAR TODAS LAS FUNCIONES DEL SISTEMA
    # -------------------------------------------------------
    def update_plot(self, sistema):
        self.fig.clear()
        ax = self.fig.add_subplot(111)

        # Ejes
        ax.axhline(0, color="black")
        ax.axvline(0, color="black")

        # Límites del plano
        # Límites X siempre del sistema
        ax.set_xlim(sistema.x_min, sistema.x_max)

        # Si y_min == y_max -> dejar matplotlib decidir el rango
        if sistema.y_min == sistema.y_max:
            pass  # auto-escalado
        else:
            ax.set_ylim(sistema.y_min, sistema.y_max)


        # Dibujar todas las funciones del sistema
        for func, texto, xmin, xmax, ymin, ymax in sistema.funciones:
            try:
                # Crear array de X
                xs = np.linspace(xmin, xmax, 400)

                # Evaluar función
                ys = sistema.evaluar(func, xs)

                if ys is None:
                    print(f"Función '{texto}' no válida.")
                    continue

                ys = np.array(ys, dtype=float)

                # Valores inválidos → NaN
                ys[~np.isfinite(ys)] = np.nan

                # Aplicar límites en eje Y solo si están definidos
                if ymin is not None or ymax is not None:
                    ys = np.clip(
                        ys,
                        ymin if ymin is not None else -np.inf,
                        ymax if ymax is not None else  np.inf
                    )

                ax.plot(xs, ys, label=texto)

            except Exception as e:
                print("Error graficando función:", texto, "→", e)
                continue

        ax.grid(True)
        ax.legend()
        self.canvas.draw()


    # -------------------------------------------------------
    # LIMPIAR
    # -------------------------------------------------------
    def limpiar(self):
        self.fig.clear()
        self.canvas.draw()
