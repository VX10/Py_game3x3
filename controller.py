from PyQt5.QtCore import QObject, QTimer


class Controller(QObject):
    '''
    Класс "Controller" - получает ввод от игрока и обновляет модель. Также содержит игровой цикл
    '''

    def __init__(self, model):
        super().__init__()
        self.model = model

        # таймер тика шагов
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

    def update_time(self):
        self.model.step()
        pass

    def handleKeyPress(self, event):
        pass
