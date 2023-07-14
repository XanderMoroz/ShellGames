from ShellGames.Sea_Battle.elements.dot import Dot


class Ship:
    "Базовый класс корабля"

    def __init__(self, nose_point, length, dimention):
        """
        Конструктор объекта класса Ship
        :param length: длина корабля - целочисленное значение
        :param nose_point: точка "носа" корабля - обьект класса Dot
        :param dimention: направление расположения (горизонтальное или вертикальное)
        """
        self.nose_point = nose_point
        self.length = length
        self.dimention = dimention
        self.health_point = length

    @property
    def dots(self):
        "Возвращает список всех точек корабля"
        ship_dots = []
        for dot in range(self.length):
            ship_dot_x = self.nose_point.x
            ship_dot_y = self.nose_point.y

            if self.dimention == 0:
                ship_dot_x += dot

            elif self.dimention == 1:
                ship_dot_y += dot

            ship_dots.append(Dot(ship_dot_x, ship_dot_y))

        return ship_dots

    def check_shoot(self, shot_coord):
        return shot_coord in self.dots