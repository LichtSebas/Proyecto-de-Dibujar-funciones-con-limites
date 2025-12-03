from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton

from panel_controles import PanelControles
from plotter import PlotWidget
from sistema_funciones import SistemaFunciones


class VentanaPrincipal(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Graficador Matemático - Licht")

        # Sistema matemático
        self.sistema = SistemaFunciones()

        # Widget de graficación
        self.canvas = PlotWidget()

        # Panel lateral
        self.panel = PanelControles(self)

        # Layout principal
        contenedor = QWidget()
        layout = QHBoxLayout(contenedor)

        layout.addWidget(self.panel)
        layout.addWidget(self.canvas, 1)

        self.setCentralWidget(contenedor)

        # Conectar señal del panel → actualización de gráfico
        self.panel.signal_update_plot.connect(self.actualizar_plot)

    def actualizar_plot(self):
        """Recibe la señal del panel y actualiza la gráfica completa."""
        self.canvas.update_plot(self.sistema)

    def limpiar(self):
        """Limpiar funciones y lienzo."""
        self.sistema.funciones.clear()
        self.canvas.limpiar()