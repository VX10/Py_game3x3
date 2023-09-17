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
    field_cells = []
    cell_coordinates = [[10, 10], [110, 10], [210, 10],
                        [10, 110], [110, 110], [210, 110],
                        [10, 210], [110, 210], [210, 210]]

    def __init__(self, model):
        super().__init__()
        self.model = model
        for index in range(3):
            self.field_cells.append(FieldCell(0))
            self.field_cells.append(FieldCell(1))
            self.field_cells.append(FieldCell(2))
        for index in range(9):
            self.field_cells[index].cell_coordinates = self.cell_coordinates[index]


    def paintEvent(self, event):
        painter = QPainter(self)
        for count in range(9):
            self.field_cells[count].draw_rect(painter)
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
        self.setGeometry(100, 100, 800, 600)

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
