import random


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
        self.path_list = [self.coordinate_x, self.coordinate_y]
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
                    or self.coordinate_x == 4):
                self.out_range = True
            self.path_list.append([self.coordinate_x, self.coordinate_y])



