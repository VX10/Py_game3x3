import random
import sys
from field_cell import FieldCell
from creature import Creature
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QLabel
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor, QPolygon, QFont
from PyQt5.QtCore import Qt, QObject, pyqtSignal, QPoint, QTimer


class Model(QObject):

    field_cells = None
    cell_coordinates = [[10, 10], [110, 10], [210, 10],
                        [10, 110], [110, 110], [210, 110],
                        [10, 210], [110, 210], [210, 210]]
    cell_coordinates_point = [[1, 1], [2, 1], [3, 1],
                              [1, 2], [2, 2], [3, 2],
                              [1, 3], [2, 3], [3, 3]]
    creatures_list = None

    def __init__(self):
        super().__init__()

        self.creatures_list = []
        self.field_cells = []
        for index in range(3):
            self.field_cells.append(FieldCell(0))
            self.field_cells.append(FieldCell(1))
            self.field_cells.append(FieldCell(2))
        self.shuffle_trap()

    def shuffle_trap(self):
        self.shuffle()
        # координаты ячеек
        for index in range(9):
            self.field_cells[index].cell_coordinates = self.cell_coordinates[index]
            self.field_cells[index].alarm_trap_count = 0

    def create_creature_vampus(self):
        self.creatures_list.append(Creature(0))
        self.trap_control()

    def create_creature_cat(self):
        self.creatures_list.append(Creature(1))
        self.trap_control()

    def create_creature_ghost(self):
        self.creatures_list.append(Creature(2))
        self.trap_control()

    def shuffle(self):
        random.shuffle(self.cell_coordinates)

    #
    def step(self):
        for item in self.creatures_list:
            item.step()
        self.trap_control()

    def trap_control(self):
        for item_creature in self.creatures_list:
            for item_cell in self.field_cells:
                coord_cell = self.cell_coordinates_translate(item_cell.cell_coordinates)
                coord_creature = [item_creature.coordinate_x, item_creature.coordinate_y]
                '''
                type_creature
                0 - Вампус
                1 - Кошка
                2 - Приведение

                cell_type
                0 - empty cell           / пустая ячейка
                1 - rope with a bell     / веревочка с колокольчиком
                2 - protoplasm detector  / детектор протоплазмы

                •	Веревочка с колокольчиком. Активируется вампусом и на 50% - кошкой (то есть кошка должна пройти 2 раза, чтобы ловушка сработала).
                •	Детектор протоплазмы. Активируется приведением и 50% - кошкой.
                '''
                if coord_cell == coord_creature:
                    # веревочка с колокольчиком
                    if item_cell.cell_type == 1:
                        # Вампус
                        if item_creature.type_creature == 0: item_cell.alarm_trap_count += 100
                        # Кошка
                        if item_creature.type_creature == 1: item_cell.alarm_trap_count += 50
                    # детектор протоплазмы
                    if item_cell.cell_type == 2:
                        # Приведение
                        if item_creature.type_creature == 2: item_cell.alarm_trap_count += 100
                        # Кошка
                        if item_creature.type_creature == 1: item_cell.alarm_trap_count += 50

    def clear_track(self):
        for item in self.creatures_list:
            item.path_list = []

    def cell_coordinates_translate(self, cell_coordinate):
        coordinate_out = None
        if cell_coordinate == [10, 10]: coordinate_out = [1, 1]
        if cell_coordinate == [110, 10]: coordinate_out = [2, 1]
        if cell_coordinate == [210, 10]: coordinate_out = [3, 1]

        if cell_coordinate == [10, 110]: coordinate_out = [1, 2]
        if cell_coordinate == [110, 110]: coordinate_out = [2, 2]
        if cell_coordinate == [210, 110]: coordinate_out = [3, 2]

        if cell_coordinate == [10, 210]: coordinate_out = [1, 3]
        if cell_coordinate == [110, 210]: coordinate_out = [2, 3]
        if cell_coordinate == [210, 210]: coordinate_out = [3, 3]
        return coordinate_out


class View(QWidget):

    def __init__(self, model):
        super().__init__()
        self.model = model

        self.label = QLabel("Веревочка с колокольчиком", self)
        self.label.move(110, 340)
        font = QFont()
        font.setPointSize(10)
        self.label.setFont(font)

        self.label = QLabel("Детектор протоплазмы", self)
        self.label.move(110, 416)
        font = QFont()
        font.setPointSize(10)
        self.label.setFont(font)

        self.btn_track_clear = QPushButton("Стереть траектории", self)
        self.btn_track_clear.setFixedWidth(300)
        self.btn_track_clear.move(10, 470)
        self.btn_track_clear.clicked.connect(self.model.clear_track)

        self.btn_trap_shuffle = QPushButton("Перетасовать ловушки", self)
        self.btn_trap_shuffle.setFixedWidth(300)
        self.btn_trap_shuffle.move(10, 500)
        self.btn_trap_shuffle.clicked.connect(self.model.shuffle_trap)

        self.btn_cat_run = QPushButton("Запустить кошку", self)
        self.btn_cat_run.setFixedWidth(300)
        self.btn_cat_run.move(10, 540)
        self.btn_cat_run.clicked.connect(self.model.create_creature_cat)

        self.btn_vampus_run = QPushButton("Запустить вампуса", self)
        self.btn_vampus_run.setFixedWidth(300)
        self.btn_vampus_run.move(10, 570)
        self.btn_vampus_run.clicked.connect(self.model.create_creature_vampus)

        self.btn_ghost_run = QPushButton("Запустить приведение", self)
        self.btn_ghost_run.setFixedWidth(300)
        self.btn_ghost_run.move(10, 600)
        self.btn_ghost_run.clicked.connect(self.model.create_creature_ghost)

        self.btn_tic = QPushButton("Шаг", self)
        self.btn_tic.move(10, 650)
        self.btn_tic.clicked.connect(self.model.step)

    def draw_hint(self, painter):
        painter.setPen(QPen(QColor(0, 0, 0), 5))
        painter.setBrush(QColor(255, 255, 220))
        # ромб (веревочка с колокольчиком)
        points = QPolygon([
            QPoint(1 + 50, 300 + 20),  # Вершина A
            QPoint(1 + 90, 300 + 50),  # Вершина B
            QPoint(1 + 50, 300 + 80),  # Вершина C
            QPoint(1 + 10, 300 + 50)   # Вершина D
        ])
        painter.setPen(QPen(Qt.black, 5))
        painter.drawPolygon(points)

        # звезда (детектор протоплазмы)
        points = QPolygon([
            QPoint(1 + 50, 375 + 10),
            QPoint(1 + 60, 375 + 40),
            QPoint(1 + 90, 375 + 50),
            QPoint(1 + 60, 375 + 60),
            QPoint(1 + 50, 375 + 90),
            QPoint(1 + 40, 375 + 60),
            QPoint(1 + 10, 375 + 50),
            QPoint(1 + 40, 375 + 40)
        ])
        painter.setPen(QPen(Qt.black, 5))
        painter.drawPolygon(points)
        pass

    def paintEvent(self, event):
        painter = QPainter(self)

        for count in range(9):
            self.model.field_cells[count].draw_rect(painter)

        for item in self.model.creatures_list:
            item.draw_track(painter)

        for item in self.model.creatures_list:
            item.draw_creature(painter)
        self.draw_hint(painter)
        self.update()
        pass


class Controller(QObject):
    def __init__(self, model):
        super().__init__()
        self.model = model

        # таймер тика программы
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

    def update_time(self):
        self.model.step()
        pass

    def handleKeyPress(self, event):
        pass


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Задание")
        self.setGeometry(100, 100, 320, 700)
        self.setFixedSize(320, 700)

        model = Model()
        view = View(model)
        controller = Controller(model)

        self.keyPressEvent = controller.handleKeyPress

        self.setCentralWidget(view)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
