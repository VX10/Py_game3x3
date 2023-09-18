import random
import sys
from field_cell import FieldCell
from creature import Creature
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor
from PyQt5.QtCore import Qt, QObject, pyqtSignal


class Model(QObject):
    coordinatesChanged = pyqtSignal(int, int)

    def __init__(self):
        super().__init__()
        self.square_x = 100
        self.square_y = 100

    def updateCoordinates(self, direction):
        step = 10
        if direction == 'left':
            self.square_x -= step
        elif direction == 'right':
            self.square_x += step
        elif direction == 'up':
            self.square_y -= step
        elif direction == 'down':
            self.square_y += step
        self.coordinatesChanged.emit(self.square_x, self.square_y)


class View(QWidget):
    field_cells = []
    cell_coordinates = [[10, 10], [110, 10], [210, 10],
                        [10, 110], [110, 110], [210, 110],
                        [10, 210], [110, 210], [210, 210]]
    cell_coordinates_point = [[1, 1], [2, 1], [3, 1],
                              [1, 2], [2, 2], [3, 2],
                              [1, 3], [2, 3], [3, 3]]
    creatures_list = None

    def __init__(self, model):
        super().__init__()
        self.model = model
        self.creatures_list = []
        for index in range(3):
            self.field_cells.append(FieldCell(0))
            self.field_cells.append(FieldCell(1))
            self.field_cells.append(FieldCell(2))
        self.shuffle_trap()

        self.btn_track_clear = QPushButton("Стереть траектории", self)
        self.btn_track_clear.move(100, 350)
        self.btn_track_clear.clicked.connect(self.clear_track)

        self.btn_trap_shuffle = QPushButton("Перетасовать ловушки", self)
        self.btn_trap_shuffle.move(100, 400)
        self.btn_trap_shuffle.clicked.connect(self.shuffle_trap)

        self.btn_vampus_run = QPushButton("Запустить вампуса", self)
        self.btn_vampus_run.move(100, 550)
        self.btn_vampus_run.clicked.connect(self.create_creature_vampus)

        self.btn_cat_run = QPushButton("Запустить кошку", self)
        self.btn_cat_run.move(100, 500)
        self.btn_cat_run.clicked.connect(self.create_creature_cat)

        self.btn_ghost_run = QPushButton("Запустить приведение", self)
        self.btn_ghost_run.move(100, 600)
        self.btn_ghost_run.clicked.connect(self.create_creature_ghost)

        self.btn_tic = QPushButton("Шаг", self)
        self.btn_tic.move(100, 650)
        self.btn_tic.clicked.connect(self.step)

    def shuffle_trap(self):
        self.shuffle()
        for index in range(9):
            self.field_cells[index].cell_coordinates = self.cell_coordinates[index]
            self.field_cells[index].alarm_trap_count = 0
        self.update()

    def create_creature_vampus(self):
        self.creatures_list.append(Creature(0))
        self.trap_control()
        self.update()
        pass

    def create_creature_cat(self):
        self.creatures_list.append(Creature(1))
        self.trap_control()
        self.update()


    def create_creature_ghost(self):
        self.creatures_list.append(Creature(2))
        self.trap_control()
        self.update()

    def shuffle(self):
        random.shuffle(self.cell_coordinates)

    def paintEvent(self, event):
        painter = QPainter(self)
        for count in range(9):
            self.field_cells[count].draw_rect(painter)
        for item in self.creatures_list:
            item.draw_track(painter)
        for item in self.creatures_list:
            item.draw_creature(painter)
        pass

    def step(self):
        for item in self.creatures_list:
            item.step()
        self.trap_control()
        self.update()

    def trap_control(self):
        for item_creature in self.creatures_list:
            for item_cell in self.field_cells:
                coord_cell = self.cell_coordinates_translate(item_cell.cell_coordinates)
                coord_creature = [item_creature.coordinate_x, item_creature.coordinate_y]
                # type_creature
                # 0 - Вампус
                # 1 - Кошка
                # 2 - Приведение

                # cell_type
                # 0 - empty cell           / пустая ячейка
                # 1 - rope with a bell     / веревочка с колокольчиком
                # 2 - protoplasm detector  / детектор протоплазмы

                # •	Веревочка с колокольчиком. Активируется вампусом и на 50% - кошкой (то есть кошка должна пройти 2 раза, чтобы ловушка сработала).
                # •	Детектор протоплазмы. Активируется приведением и 50% - кошкой.
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
        self.update()

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



class Controller(QObject):
    def __init__(self, model):
        super().__init__()
        self.model = model

    def handleKeyPress(self, event):
        if event.key() == Qt.Key_Left:
            self.model.updateCoordinates('left')
        elif event.key() == Qt.Key_Right:
            self.model.updateCoordinates('right')
        elif event.key() == Qt.Key_Up:
            self.model.updateCoordinates('up')
        elif event.key() == Qt.Key_Down:
            self.model.updateCoordinates('down')


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Задание")
        self.setGeometry(100, 100, 320, 700)
        self.setFixedSize(320, 700)

        model = Model()
        view = View(model)
        controller = Controller(model)

        model.coordinatesChanged.connect(view.update)

        self.setCentralWidget(view)
        self.keyPressEvent = controller.handleKeyPress


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
