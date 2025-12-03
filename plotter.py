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
        ax.set_xlim(sistema.x_min, sistema.x_max)
        ax.set_ylim(sistema.y_min, sistema.y_max)

        # Dibujar todas las funciones del sistema
        for func, texto, xmin, xmax in sistema.funciones:

            try:
                xs = np.linspace(xmin, xmax, 400)

                # Evaluar con la función segura
                ys = func(xs)

                # Si eval devolvió None → NO se dibuja
                if ys is None:
                    print(f"Función '{texto}' no válida.")
                    continue

                # Filtrar valores no válidos
                ys = np.array(ys, dtype=float)
                ys[~np.isfinite(ys)] = np.nan

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
