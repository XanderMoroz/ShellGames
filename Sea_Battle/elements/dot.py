

class Dot:
    "Базовый класс точки на игровом поле"

    def __init__(self, x, y):
        """
        Конструктор обьекта класса Dot
        :param x: координата точки по горизонтали - целочисленное значение.
        :param y: координата точки по вертикали - целочисленное значение.
        """
        self.x = x
        self.y = y

    def __eq__(self, other_dot):
        """
        Метод сравнивает координаты точки с координатами другой точки.
        :param other_dot: объект класса Dot
        :return: True если координаты точек совпадают и False если не совпадают.
        """
        return self.x == other_dot.x and self.y == other_dot.y
    def __repr__(self):
        return f"Dot({self.x}, {self.y})"
