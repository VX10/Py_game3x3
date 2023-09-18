import random
from field_cell import FieldCell
from creature import Creature
from PyQt5.QtCore import QObject


class Model(QObject):
    '''
    Класс "Model" - содержит данные и состояние. Отвечает за обновление игровой логики
    '''
    field_cells = None
    cell_coordinates = [[10, 10], [110, 10], [210, 10],
                        [10, 110], [110, 110], [210, 110],
                        [10, 210], [110, 210], [210, 210]]
    cell_coordinates_point = [[1, 1], [2, 1], [3, 1],
                              [1, 2], [2, 2], [3, 2],
                              [1, 3], [2, 3], [3, 3]]
    creatures_list = None

    def __init__(self):
        super().__init__()

        self.creatures_list = []
        self.field_cells = []
        for index in range(3):
            self.field_cells.append(FieldCell(0))
            self.field_cells.append(FieldCell(1))
            self.field_cells.append(FieldCell(2))
        self.shuffle_trap()

    def shuffle_trap(self):
        '''
        Метод перетасовывает ячейки с ловушками
        '''
        random.shuffle(self.cell_coordinates)
        # координаты ячеек
        for index in range(9):
            self.field_cells[index].cell_coordinates = self.cell_coordinates[index]
            self.field_cells[index].alarm_trap_count = 0

    def create_creature_vampus(self):
        '''
        Метод создаёт объект сущности "Вампус"
        '''
        self.creatures_list.append(Creature(0))
        self.trap_control()

    def create_creature_cat(self):
        '''
        Метод создаёт объект сущности "Кошка"
        '''
        self.creatures_list.append(Creature(1))
        self.trap_control()

    def create_creature_ghost(self):
        '''
        Метод создаёт объект сущности "Приведение"
        '''
        self.creatures_list.append(Creature(2))
        self.trap_control()

    #
    def step(self):
        '''
        Метод инициирует 1 шаг всех сущьностей
        '''
        for item in self.creatures_list:
            item.step()
        self.trap_control()

    def trap_control(self):
        '''
        Метод контролирует срабатывания ловушки в соответсвии правилам
        type_creature
        0 - Вампус
        1 - Кошка
        2 - Приведение

        cell_type
        0 - empty cell           / пустая ячейка
        1 - rope with a bell     / веревочка с колокольчиком
        2 - protoplasm detector  / детектор протоплазмы

        •	Веревочка с колокольчиком. Активируется вампусом и на 50% - кошкой (то есть кошка должна пройти 2 раза, чтобы ловушка сработала).
        •	Детектор протоплазмы. Активируется приведением и 50% - кошкой.
        '''
        for item_creature in self.creatures_list:
            for item_cell in self.field_cells:
                coord_cell = self.cell_coordinates_translate(item_cell.cell_coordinates)
                coord_creature = [item_creature.coordinate_x, item_creature.coordinate_y]
                if coord_cell == coord_creature:
                    # веревочка с колокольчиком
                    if item_cell.cell_type == 1:
                        # Вампус
                        if item_creature.type_creature == 0: item_cell.alarm_trap_count += 100
                        # Кошка
                        if item_creature.type_creature == 1: item_cell.alarm_trap_count += 50
                    # детектор протоплазмы
                    if item_cell.cell_type == 2:
                        # Приведение
                        if item_creature.type_creature == 2: item_cell.alarm_trap_count += 100
                        # Кошка
                        if item_creature.type_creature == 1: item_cell.alarm_trap_count += 50

    def clear_track(self):
        '''
        Метод траекторий сущьностей
        '''
        for item in self.creatures_list:
            item.path_list = []

    def cell_coordinates_translate(self, cell_coordinate):
        '''
        Метод перевода координат ячеек на поле в параметры соостветсвия двумерного массава списка
        '''
        coordinate_out = None
        if cell_coordinate == [10, 10]: coordinate_out = [1, 1]
        if cell_coordinate == [110, 10]: coordinate_out = [2, 1]
        if cell_coordinate == [210, 10]: coordinate_out = [3, 1]

        if cell_coordinate == [10, 110]: coordinate_out = [1, 2]
        if cell_coordinate == [110, 110]: coordinate_out = [2, 2]
        if cell_coordinate == [210, 110]: coordinate_out = [3, 2]

        if cell_coordinate == [10, 210]: coordinate_out = [1, 3]
        if cell_coordinate == [110, 210]: coordinate_out = [2, 3]
        if cell_coordinate == [210, 210]: coordinate_out = [3, 3]
        return coordinate_out
