from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor
from PyQt5.QtCore import Qt, QObject, pyqtSignal


class FieldCell(QWidget):
    '''
    Класс ячейки игового поля
    '''
    coordinate_x = None
    coordinate_y = None
    cell_type = None

    # def __init__(self, cell_type=0):
    #     self.cell_type = cell_type

    def DrawRect(self):
        pass

        qp = QPainter(self)
        qp.setPen(QPen(Qt.black, 2))
        brush = QBrush(Qt.red)
        qp.setBrush(brush)
        qp.drawRect(10, 10, 100, 100)
