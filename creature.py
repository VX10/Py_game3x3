import random

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPen


class Creature:
    '''
    Класс существ (type_creature):
    0 - Вампус
    1 - Кошка
    2 - Приведение
    '''
    type_creature = None
    coordinate_x = None
    coordinate_y = None
    path_list = None
    out_range = None

    def __init__(self, type_creature):
        self.type_creature = type_creature
        self.coordinate_x = 2
        self.coordinate_y = 2
        self.path_list = [[self.coordinate_x, self.coordinate_y]]
        self.out_range = False

    def step(self):
        if not self.out_range:
            # случайное направление движения существа
            # 1 - up
            # 2 - down
            # 3 - right
            # 4 - left
            direct = random.randint(1, 4)
            if direct == 1:
                self.coordinate_y -= 1
            if direct == 2:
                self.coordinate_y += 1
            if direct == 3:
                self.coordinate_x += 1
            if direct == 4:
                self.coordinate_x -= 1
            # контроль границ
            if (self.coordinate_x == 0
                    or self.coordinate_x == 4
                    or self.coordinate_y == 0
                    or self.coordinate_y == 4):
                self.out_range = True
            self.path_list.append([self.coordinate_x, self.coordinate_y])
            pass

    def draw_creature(self, painter):
        # painter.setPen(Qt.NoPen)
        # painter.setPen(Qt.black)
        painter.setPen(QPen(QColor(0,0,0), 1))
        # цвет существа
        if self.type_creature == 0:
            painter.setBrush(QColor(0, 255, 0))
        if self.type_creature == 1:
            painter.setBrush(QColor(0, 0, 255))
        if self.type_creature == 2:
            painter.setBrush(QColor(255, 0, 0))

        if self.coordinate_x == 1 and self.coordinate_y == 1:
            painter.drawEllipse(60 - 20, 60 - 20, 40, 40)

        if self.coordinate_x == 1 and self.coordinate_y == 2:
            painter.drawEllipse(60 - 20, 160 - 20, 40, 40)

        if self.coordinate_x == 1 and self.coordinate_y == 3:
            painter.drawEllipse(60 - 20, 260 - 20, 40, 40)

        if self.coordinate_x == 2 and self.coordinate_y == 1:
            painter.drawEllipse(160 - 20, 60 - 20, 40, 40)

        if self.coordinate_x == 2 and self.coordinate_y == 2:
            painter.drawEllipse(160 - 20, 160 - 20, 40, 40)

        if self.coordinate_x == 2 and self.coordinate_y == 3:
            painter.drawEllipse(160 - 20, 260 - 20, 40, 40)

        if self.coordinate_x == 3 and self.coordinate_y == 1:
            painter.drawEllipse(260 - 20, 60 - 20, 40, 40)

        if self.coordinate_x == 3 and self.coordinate_y == 2:
            painter.drawEllipse(260 - 20, 160 - 20, 40, 40)

        if self.coordinate_x == 3 and self.coordinate_y == 3:
            painter.drawEllipse(260 - 20, 260 - 20, 40, 40)

    def draw_track(self, painter):
        if len(self.path_list) < 2:
            return
        for i in range(len(self.path_list)-1):
            if self.path_list[i][0] == 0: x1 = 10
            if self.path_list[i][0] == 1: x1 = 60
            if self.path_list[i][0] == 2: x1 = 160
            if self.path_list[i][0] == 3: x1 = 260
            if self.path_list[i][0] == 4: x1 = 310

            if self.path_list[i][1] == 0: y1 = 10
            if self.path_list[i][1] == 1: y1 = 60
            if self.path_list[i][1] == 2: y1 = 160
            if self.path_list[i][1] == 3: y1 = 260
            if self.path_list[i][1] == 4: y1 = 310

            if self.path_list[i+1][0] == 0: x2 = 10
            if self.path_list[i+1][0] == 1: x2 = 60
            if self.path_list[i+1][0] == 2: x2 = 160
            if self.path_list[i+1][0] == 3: x2 = 260
            if self.path_list[i+1][0] == 4: x2 = 310

            if self.path_list[i+1][1] == 0: y2 = 10
            if self.path_list[i+1][1] == 1: y2 = 60
            if self.path_list[i+1][1] == 2: y2 = 160
            if self.path_list[i+1][1] == 3: y2 = 260
            if self.path_list[i+1][1] == 4: y2 = 310

            # цвет трека
            if self.type_creature == 0:
                painter.setPen(QPen(QColor(0, 255, 0), 7))
            if self.type_creature == 1:
                painter.setPen(QPen(QColor(0, 0, 255), 7))
            if self.type_creature == 2:
                painter.setPen(QPen(QColor(255, 0, 0), 7))

            # Рисуем линию от (x1, y1) до (x2, y2)
            painter.drawLine(x1, y1, x2, y2)
        pass
