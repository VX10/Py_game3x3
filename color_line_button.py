from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QPainter, QPen


class ColorLineButton(QPushButton):
    '''
    Класc "Кнопки" с цветной линией
    '''

    def __init__(self, text, parent, qt_color, x1, y1, x2, y2):
        super().__init__(text, parent)
        self.line_color = qt_color
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        pass

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        pen = QPen(self.line_color)
        pen.setWidth(5)
        painter.setPen(pen)
        painter.drawLine(self.x1, self.y1, self.x2, self.y2)
