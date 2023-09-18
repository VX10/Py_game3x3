import sys
from main_window import MainWindow
from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    '''
    Главная функция - точка входа
    '''
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
