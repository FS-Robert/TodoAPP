# Importamos sys y las clases de PyQt5 necesarias para crear la ventana,
# mostrar texto, recibir entradas, botones, listas, mensajes y un ícono.
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QListWidget, QMessageBox, 
)
from PyQt5.QtGui import QIcon


class ToDoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lista de Tareas")
        self.setGeometry(200, 200, 400, 300)
     # Icono de la aplicación
        self.setWindowIcon(QIcon('logo.png'))  # Icono de la aplicación
    # --- Widgets básicos ---
        self.label = QLabel("Escribe tu tarea:")    # Etiqueta
        self.tarea_input = QLineEdit()              # Campo de entrada de texto
        self.tarea_input.setPlaceholderText("Ejemplo: Hacer la tarea de matemáticas")
        self.add_button = QPushButton("Agregar tarea")     # Botón para agregar
        self.delete_button = QPushButton("Eliminar tarea") # Botón para eliminar
        self.done_button = QPushButton("Marcar como completada")  # Botón para marcar como hecha
        self.task_list = QListWidget()    # Lista donde se muestran las tareas
        self.info_label = QLabel("Total tareas: 0 | Completadas: 0") # Etiqueta con estadísticas
        
    # --- Layouts (organización en pantalla) ---
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.tarea_input)
        input_layout.addWidget(self.add_button)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.done_button)
        button_layout.addWidget(self.delete_button)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.label)
        main_layout.addLayout(input_layout)
        main_layout.addWidget(self.task_list)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.info_label)

        self.setLayout(main_layout)

         # --- Conexiones de botones con funciones ---
        self.add_button.clicked.connect(self.add_task)
        self.delete_button.clicked.connect(self.delete_task)
        self.done_button.clicked.connect(self.complete_task)

        # Contadores
        self.total_tasks = 0
        self.completed_tasks = 0

        # --- Cargar tareas previas desde archivo ---
        self.cargar_tareas()

     # --- Función para agregar una tarea ---
        task = self.tarea_input.text().strip()
        if task:
            self.task_list.addItem(task) # Se agrega a la lista
            self.tarea_input.clear()   # Se limpia el input
            self.total_tasks += 1     # Se aumenta contador
            self.update_info()
            self.guardar_tareas()
        else:
            QMessageBox.warning(self, "Error", "Debes escribir una tarea.")
    # --- Función para eliminar tarea seleccionada ---
    def delete_task(self):
        selected_item = self.task_list.currentItem()
        if selected_item:
            self.task_list.takeItem(self.task_list.row(selected_item))
            self.total_tasks -= 1
            self.update_info()
            self.guardar_tareas()
        else:
            QMessageBox.warning(self, "Error", "Selecciona una tarea para eliminar.")
    # --- Función para marcar como completada ---
    def complete_task(self):
        selected_item = self.task_list.currentItem()
        if selected_item:
            if not selected_item.text().startswith("[✔]"):
                selected_item.setText(f"[✔] {selected_item.text()}")
                self.completed_tasks += 1
                self.update_info()
                self.guardar_tareas()
        else:
            QMessageBox.warning(self, "Error", "Selecciona una tarea para marcar como completada.")
# --- Actualizar la etiqueta de información ---
    def update_info(self):
        self.info_label.setText(f"Total tareas: {self.total_tasks} | Completadas: {self.completed_tasks}")
    # --- Guardar las tareas en un archivo ---

    def guardar_tareas(self):
        with open("tareas.txt", "w", encoding="utf-8") as f:
            for i in range(self.task_list.count()):
                f.write(self.task_list.item(i).text() + "\n")
    # --- Cargar tareas desde archivo si existe ---

    def cargar_tareas(self):
        try:
            with open("tareas.txt", "r", encoding="utf-8") as f:
                for linea in f:
                    tarea = linea.strip()
                    self.task_list.addItem(tarea)
                    self.total_tasks += 1
                    if tarea.startswith("[✔]"):
                        self.completed_tasks += 1
            self.update_info()
        except FileNotFoundError:
            pass  # si no existe el archivo, no hace nada


# --- Ejecución del programa ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = ToDoApp()
    ventana.show()
    sys.exit(app.exec_())
