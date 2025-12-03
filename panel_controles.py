from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QLabel, QPushButton, QComboBox, QListWidget, QHBoxLayout, QListWidgetItem
from PyQt5.QtCore import pyqtSignal

class PanelControles(QWidget):

    signal_update_plot = pyqtSignal()

    def __init__(self, main_window):
        super().__init__()

        self.main = main_window
        self.sistema = main_window.sistema

        layout = QVBoxLayout()

        # -------------------------
        # Agregar función
        # -------------------------
        layout.addWidget(QLabel("Función f(x):"))
        self.input_funcion = QLineEdit()
        self.input_funcion.setPlaceholderText("sin(x) + x**2")
        layout.addWidget(self.input_funcion)

        self.input_xmin = QLineEdit()
        self.input_xmin.setPlaceholderText("xmin")
        self.input_xmax = QLineEdit()
        self.input_xmax.setPlaceholderText("xmax")

        layout.addWidget(self.input_xmin)
        layout.addWidget(self.input_xmax)

        self.btn_agregar = QPushButton("Agregar función")
        self.btn_agregar.clicked.connect(self.agregar_funcion)
        layout.addWidget(self.btn_agregar)

        # -------------------------
        # Lista de funciones
        # -------------------------
        layout.addWidget(QLabel("Funciones agregadas:"))
        self.lista = QListWidget()
        layout.addWidget(self.lista)

        self.btn_eliminar = QPushButton("Eliminar función seleccionada")
        self.btn_eliminar.clicked.connect(self.eliminar_funcion)
        layout.addWidget(self.btn_eliminar)

        # -------------------------
        # Limpiar todo
        # -------------------------
        self.btn_limpiar = QPushButton("Limpiar todo")
        self.btn_limpiar.clicked.connect(self.limpiar_todo)
        layout.addWidget(self.btn_limpiar)

        # -------------------------
        # Límites del plano
        # -------------------------
        layout.addWidget(QLabel("Límites del plano:"))
        self.input_xmin_plano = QLineEdit(); self.input_xmin_plano.setPlaceholderText("X min")
        self.input_xmax_plano = QLineEdit(); self.input_xmax_plano.setPlaceholderText("X max")
        self.input_ymin_plano = QLineEdit(); self.input_ymin_plano.setPlaceholderText("Y min")
        self.input_ymax_plano = QLineEdit(); self.input_ymax_plano.setPlaceholderText("Y max")

        for w in [self.input_xmin_plano, self.input_xmax_plano, self.input_ymin_plano, self.input_ymax_plano]:
            layout.addWidget(w)

        self.btn_actualizar = QPushButton("Actualizar plano")
        self.btn_actualizar.clicked.connect(self.actualizar_plano)
        layout.addWidget(self.btn_actualizar)

        # -------------------------
        # Métodos de cálculo
        # -------------------------
        layout.addWidget(QLabel("Método de cálculo"))
        self.combo_metodo = QComboBox()
        self.combo_metodo.addItems(["Simpson 1/3", "Trapecios", "Sólido de revolución"])
        layout.addWidget(self.combo_metodo)

        self.btn_calcular = QPushButton("Calcular")
        self.btn_calcular.clicked.connect(self.calcular)
        layout.addWidget(self.btn_calcular)

        self.lbl_resultado = QLabel("Resultado:")
        layout.addWidget(self.lbl_resultado)

        self.setLayout(layout)

    # ----------------------------------------------------------
    # AGREGAR FUNCIÓN
    # ----------------------------------------------------------
    def agregar_funcion(self):
        texto = self.input_funcion.text().strip()
        if texto == "":
            self.lbl_resultado.setText("Error: función vacía")
            return

        try:
            xmin = float(self.input_xmin.text())
            xmax = float(self.input_xmax.text())
        except:
            self.lbl_resultado.setText("Error: límites inválidos")
            return

        # ---------------------------------------------
        # Convertir TEXTO a FUNCIÓN PYTHON
        # ---------------------------------------------
        try:
            import numpy as np
            funcion = eval(f"lambda x: {texto}", {"np": np, "sin": np.sin, "cos": np.cos, "tan": np.tan})
        except Exception as e:
            self.lbl_resultado.setText(f"Error en función: {e}")
            return

        # Guardar en el sistema como: (funcion_callable, texto_original, xmin, xmax)
        self.sistema.funciones.append((funcion, texto, xmin, xmax))

        # ---------------------------------------------
        # Crear item visual
        # ---------------------------------------------
        item = QListWidgetItem()
        widget = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)

        label = QLabel(f"{texto}  |  [{xmin}, {xmax}]")
        btn_edit = QPushButton("✏")
        btn_del = QPushButton("✖")

        btn_edit.setFixedWidth(30)
        btn_del.setFixedWidth(30)

        index = len(self.sistema.funciones) - 1

        btn_edit.clicked.connect(lambda _, i=index: self.editar_funcion(i))
        btn_del.clicked.connect(lambda _, i=index: self.eliminar_funcion_directo(i))

        layout.addWidget(label)
        layout.addWidget(btn_edit)
        layout.addWidget(btn_del)

        widget.setLayout(layout)
        item.setSizeHint(widget.sizeHint())
        self.lista.addItem(item)
        self.lista.setItemWidget(item, widget)

        self.signal_update_plot.emit()


    # ----------------------------------------------------------
    # ELIMINAR FUNCIÓN
    # ----------------------------------------------------------
    def eliminar_funcion(self):
        fila = self.lista.currentRow()
        if fila >= 0:
            del self.sistema.funciones[fila]
            self.lista.takeItem(fila)
            self.signal_update_plot.emit()

    # ----------------------------------------------------------
    # ACTUALIZAR PLANO
    # ----------------------------------------------------------
    def actualizar_plano(self):
        x1_text = self.input_xmin_plano.text().strip()
        x2_text = self.input_xmax_plano.text().strip()
        y1_text = self.input_ymin_plano.text().strip()
        y2_text = self.input_ymax_plano.text().strip()

        # Mantener límites actuales si están vacíos
        try:
            x1 = float(x1_text) if x1_text != "" else self.sistema.x_min
            x2 = float(x2_text) if x2_text != "" else self.sistema.x_max
            y1 = float(y1_text) if y1_text != "" else self.sistema.y_min
            y2 = float(y2_text) if y2_text != "" else self.sistema.y_max
        except:
            self.lbl_resultado.setText("Error en límites del plano")
            return

        self.sistema.configurar_plano(x1, x2, y1, y2)
        self.signal_update_plot.emit()

    # ----------------------------------------------------------
    # CALCULAR
    # ----------------------------------------------------------
    def calcular(self):
        if len(self.sistema.funciones) == 0:
            self.lbl_resultado.setText("No hay funciones")
            return

        metodo = self.combo_metodo.currentText()
        func, texto, xmin, xmax = self.sistema.funciones[-1]

        try:
            if metodo == "Simpson 1/3":
                r = self.sistema.area_simpson(texto, xmin, xmax)
            elif metodo == "Trapecios":
                r = self.sistema.area_trapecios(texto, xmin, xmax)
            else:
                r = self.sistema.solido_revolucion(texto, xmin, xmax)

            self.lbl_resultado.setText(f"Resultado: {r:.4f}")

        except Exception as e:
            self.lbl_resultado.setText(f"Error: {e}")

    # ----------------------------------------------------------
    # LIMPIAR TODO
    # ----------------------------------------------------------
    def limpiar_todo(self):
        self.sistema.funciones.clear()
        self.lista.clear()
        self.main.limpiar()
        self.signal_update_plot.emit()

    # ----------------------------------------------------------
    # Eliminar función directo (sin usar selección)
    # ----------------------------------------------------------
    def eliminar_funcion_directo(self, index):
        del self.sistema.funciones[index]
        self.lista.takeItem(index)
        self.signal_update_plot.emit()
    # ----------------------------------------------------------
    # Editar función
    # ----------------------------------------------------------
    def editar_funcion(self, index):
        func, texto, xmin, xmax = self.sistema.funciones[index]

        # poner datos en inputs
        self.input_funcion.setText(texto)
        self.input_xmin.setText(str(xmin))
        self.input_xmax.setText(str(xmax))

        # eliminar el antiguo
        self.eliminar_funcion_directo(index)