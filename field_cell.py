from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtGui import QPainter, QPolygon, QBrush, QColor, QPen
from PyQt5.QtCore import Qt, QObject, pyqtSignal, QPoint


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
        painter.setPen(QPen(QColor(0, 0, 0), 5))
        painter.setBrush(QColor(255, 0, 0))
        painter.drawRect(self.cell_coordinates[0], self.cell_coordinates[1], size, size)

        if self.cell_type == 0 or self.cell_type == 1 or self.cell_type == 2:
            points = QPolygon([
                QPoint(self.cell_coordinates[0] + 50, self.cell_coordinates[1] + 20),   # Вершина A
                QPoint(self.cell_coordinates[0] + 90, self.cell_coordinates[1] + 50),   # Вершина B
                QPoint(self.cell_coordinates[0] + 50, self.cell_coordinates[1] + 80),   # Вершина C
                QPoint(self.cell_coordinates[0] + 10, self.cell_coordinates[1] + 50)    # Вершина D
            ])
            # painter.setPen(Qt.black)  # Устанавливаем цвет линии
            painter.setPen(QPen(Qt.black, 5))
            painter.setBrush(QColor(255, 0, 0))  # Устанавливаем цвет заливки (красный)
            painter.drawPolygon(points)  # Рисуем ромб
            pass
