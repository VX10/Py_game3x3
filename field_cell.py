from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor
from PyQt5.QtCore import Qt, QObject, pyqtSignal


class FieldCell():
    '''
    Класс ячейки игового поля
    '''
    coordinate_x = None
    coordinate_y = None
    # cell_type
    # 0 - empty cell           / пустая ячейка
    # 1 - rope with a bell     / веревочка с колокольчиком
    # 2 - protoplasm detector  / детектор протоплазмы
    cell_type = None
    painter = None

    def __init__(self, cell_type):
        self.cell_type = cell_type

    def draw_rect(self):
        pass

        size = 100
        self.painter.setPen(Qt.black)
        self.painter.setBrush(QColor(255, 0, 0))
        self.painter.drawRect(10, 10, size, size)
