from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor
from PyQt5.QtCore import Qt, QObject, pyqtSignal


class FieldCell():
    '''
    Класс ячейки игового поля
    '''
    # cell_coordinates = [x, y]
    cell_coordinates = []
    # cell_type
    # 0 - empty cell           / пустая ячейка
    # 1 - rope with a bell     / веревочка с колокольчиком
    # 2 - protoplasm detector  / детектор протоплазмы
    cell_type = None

    def __init__(self, cell_type):
        self.cell_type = cell_type

    def draw_rect(self, painter):
        pass

        size = 100
        # Настраиваем параметры пера
        pen = painter.pen()
        pen.setWidth(3)  # Устанавливаем толщину линии в 3px
        painter.setPen(pen)

        painter.setBrush(QColor(255, 0, 0))
        painter.drawRect(self.cell_coordinates[0], self.cell_coordinates[1], size, size)
