from color_line_button import ColorLineButton
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel
from PyQt5.QtGui import QPainter, QPen, QColor, QPolygon, QFont
from PyQt5.QtCore import Qt, QPoint


class View(QWidget):
    '''
    Класс "View" - отвечает за отрисовку. Обращается к модели за данными для визуализации
    '''

    def __init__(self, model):
        super().__init__()
        self.model = model

        self.label = QLabel("Веревочка с колокольчиком", self)
        self.label.move(110, 340)
        font = QFont()
        font.setPointSize(10)
        self.label.setFont(font)

        self.label = QLabel("Детектор протоплазмы", self)
        self.label.move(110, 416)
        font = QFont()
        font.setPointSize(10)
        self.label.setFont(font)

        self.btn_track_clear = QPushButton("Стереть траектории", self)
        self.btn_track_clear.setFixedWidth(300)
        self.btn_track_clear.move(10, 470)
        self.btn_track_clear.clicked.connect(self.model.clear_track)

        self.btn_trap_shuffle = QPushButton("Перетасовать ловушки", self)
        self.btn_trap_shuffle.setFixedWidth(300)
        self.btn_trap_shuffle.move(10, 500)
        self.btn_trap_shuffle.clicked.connect(self.model.shuffle_trap)

        self.btn_cat_run = ColorLineButton("Запустить кошку", self, QColor(0, 0, 255), 20, 12, 80, 12)
        self.btn_cat_run.setFixedWidth(300)
        self.btn_cat_run.move(10, 540)
        self.btn_cat_run.clicked.connect(self.model.create_creature_cat)

        self.btn_vampus_run = ColorLineButton("Запустить вампуса", self, QColor(0, 255, 0), 20, 12, 80, 12)
        self.btn_vampus_run.setFixedWidth(300)
        self.btn_vampus_run.move(10, 570)
        self.btn_vampus_run.clicked.connect(self.model.create_creature_vampus)

        self.btn_ghost_run = ColorLineButton("Запустить приведение", self, QColor(255, 0, 0), 20, 12, 80, 12)
        self.btn_ghost_run.setFixedWidth(300)
        self.btn_ghost_run.move(10, 600)
        self.btn_ghost_run.clicked.connect(self.model.create_creature_ghost)

        # self.btn_tic = QPushButton("Шаг", self)
        # self.btn_tic.move(10, 650)
        # self.btn_tic.clicked.connect(self.model.step)

    def draw_hint(self, painter):
        '''
        Метод вывода подсказки (легенда) для пользователя
        '''
        painter.setPen(QPen(QColor(0, 0, 0), 5))
        painter.setBrush(QColor(255, 255, 220))
        # ромб (веревочка с колокольчиком)
        points = QPolygon([
            QPoint(1 + 50, 300 + 20),  # Вершина A
            QPoint(1 + 90, 300 + 50),  # Вершина B
            QPoint(1 + 50, 300 + 80),  # Вершина C
            QPoint(1 + 10, 300 + 50)  # Вершина D
        ])
        painter.setPen(QPen(Qt.black, 5))
        painter.drawPolygon(points)

        # звезда (детектор протоплазмы)
        points = QPolygon([
            QPoint(1 + 50, 375 + 10),
            QPoint(1 + 60, 375 + 40),
            QPoint(1 + 90, 375 + 50),
            QPoint(1 + 60, 375 + 60),
            QPoint(1 + 50, 375 + 90),
            QPoint(1 + 40, 375 + 60),
            QPoint(1 + 10, 375 + 50),
            QPoint(1 + 40, 375 + 40)
        ])
        painter.setPen(QPen(Qt.black, 5))
        painter.drawPolygon(points)
        pass

    def paintEvent(self, event):
        '''
        Метод обновления интерфейса
        '''
        painter = QPainter(self)

        # визуализация поля с ловушками
        for count in range(9):
            self.model.field_cells[count].draw_rect(painter)

        # визуализация существ
        for item in self.model.creatures_list:
            item.draw_track(painter)

        # визуализация траекторий сущьностей
        for item in self.model.creatures_list:
            item.draw_creature(painter)

        # визуализация "легенды"
        self.draw_hint(painter)

        self.update()
