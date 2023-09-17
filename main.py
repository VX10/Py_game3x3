import sys
from field_cell import FieldCell
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
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
    painter = None
    field_cells = []

    def __init__(self, model):
        super().__init__()
        self.model = model
        self.field_cells.append(FieldCell(0))

    def paintEvent(self, event):
        painter = QPainter(self)
        self.field_cells[0].painter = painter
        self.field_cells[0].draw_rect()
        # field_cell = FieldCell(painter)
        # field_cell.draw_rect()
        pass


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

        self.setWindowTitle("Перемещение квадрата")
        self.setGeometry(100, 100, 300, 300)

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
