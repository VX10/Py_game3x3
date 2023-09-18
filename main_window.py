from model import Model
from view import View
from controller import Controller
from PyQt5.QtWidgets import QMainWindow


class MainWindow(QMainWindow):
    '''
    Класс главного окна приложения
    '''

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Задание")
        self.setGeometry(100, 100, 320, 650)
        self.setFixedSize(320, 650)

        model = Model()
        view = View(model)
        controller = Controller(model)

        self.keyPressEvent = controller.handleKeyPress

        self.setCentralWidget(view)
