from ShellGames.Sea_Battle.elements.dot import Dot
from ShellGames.Sea_Battle.exeptions import BusyDotException, BoardOutException, BoardWrongShipException


class Board:
    "Игровое поле"

    def __init__(self, hid=False, size=6):
        """
        Конструктор игрового поля
        :param hid: "скрытость" - булево значение,
        :param size: размер - целочисленное значение
        Создает игровое поле со свойствами:
        Кол-во сбитых кораблей, список использованных координат, список координат с кораблями,"
        """
        self.size = size
        self.hid = hid
        self.shooted_ship = 0
        self.field = [['O'] * size for elem in range(size)]
        self.used_dots = []
        self.ship_in_game = []

    def __str__(self):
        result = ""
        result += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for elem, row in enumerate(self.field):
            result += f"\n{elem + 1} | " + " | ".join(row) + " |"

        if self.hid:
            result = result.replace("■", "O")
        return result

    def out(self, dot):
        """
         Метод проверки нахождения точки в границах поля. Если точка за границей, выбрасывает исключение
        :param dot: объект класса Dot
        :return: True, если точка выходит за пределы поля, и False, если не выходит.
        """
        return not ((0 <= dot.x < self.size) and (0 <= dot.y < self.size))

    def add_ship(self, ship):
        """
        Метод ставит корабль на доску. Если ставить не получается, выбрасывает исключение BoardWrongShipException
        :param ship: объект класса Ship
        :return: None
        """
        for d in ship.dots:
            if self.out(d) or d in self.used_dots:
                raise BoardWrongShipException()
        for d in ship.dots:
            self.field[d.x][d.y] = "■"
            self.used_dots.append(d)

        self.ship_in_game.append(ship)
        self.contour(ship)

    def contour(self, ship, verb = False):
        """
        Метод обводит корабль по контуру и помечает соседние точки где корабля по правилам быть не может).
        :param ship: объект класса Ship
        :param verb:
        :return: None
        """
        near_dots = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for dot in ship.dots:
            for dx, dy in near_dots:
                cur = Dot(dot.x + dx, dot.y + dy)
                if not (self.out(cur)) and cur not in self.used_dots:
                    if verb:
                        self.field[cur.x][cur.y] = "."
                    self.used_dots.append(cur)

    def shot(self, dot):
        """
        Метод делает выстрел по доске.
        При попытке выстрелить за пределы поля выбрасывает исключение BoardOutException.
        При попытке выстрелить в занятую точку выбрасывает исключение BusyDotException.
        :param dot: объект класса Dot
        :return: True, если выстрел ранил корабль, и False, если выстрел потопил корабль или если выстрел был мимо.
        """
        if self.out(dot):
            raise BoardOutException()
        if dot in self.used_dots:
            raise BusyDotException()

        self.used_dots.append(dot)

        for ship in self.ship_in_game:
            if ship.check_shoot(dot):
                ship.health_point -= 1
                self.field[dot.x][dot.y] = "X"
                if ship.health_point == 0:
                    self.shooted_ship += 1
                    self.contour(ship, verb = True)
                    print("Корабль уничтожен!")
                    return False
                else:
                    print("Корабль ранен!")
                    return True

        self.field[dot.x][dot.y] = "."
        print("Мимо!")
        return False

    def begin(self):
        "Метод очищающий переменную, где содержатся координаты занятых точек."
        self.used_dots = []