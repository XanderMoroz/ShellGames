from random import randint

from ShellGames.Sea_Battle.elements.dot import Dot
from ShellGames.Sea_Battle.exeptions import Error


class Player:
    "Общий класс игрока. Его свойства и методы наследуют дочерние классы User и AI"

    def __init__(self, my_board, enemy_board):
        """
        Конструктор объекта класса Player. Создает игровые доски для пользователя и его противника.
        :param my_board: объект класса Board
        :param enemy_board: объект класса Board
        """
        self.my_board = my_board
        self.enemy_board = enemy_board

    def ask(self):
        "Метод, спрашивает игрока, в какую клетку он делает выстрел."
        raise NotImplementedError()

    def move(self):
        """
        Получает координаты точки и пробует выстрелить по доске противника
        :return: True, если выстрел ранил корабль, и False, если выстрел потопил корабль или если выстрел был мимо.
        """
        while True:
            try:
                target = self.ask()
                repeat = self.enemy_board.shot(target)
                return repeat
            except Error as e:
                print(e)

class Ai(Player):
    "Класс AI унаследован от класса Player. "
    def ask(self):
        """
        Метод ask - выбор случайной точки.
        :return: объект класса Dot со случайными координатами.
        """
        ai_target = Dot(randint(0, 5), randint(0, 5))
        print(f"Ход компьютера: {ai_target.x + 1} {ai_target.y + 1}")
        return ai_target

class User(Player):
    "Класс User унаследован от класса Player."

    def ask(self):
        """
        Метод ask - спрашивает координаты точки из консоли.
        Проверяет полученные от пользователя значения.
        :return: координаты по которым хочет выстрелить пользователь - объект класса Dot
        """
        while True:
            cords = input("Введите координаты для выстрела: ").split()

            if len(cords) != 2:
                print(" Введите 2 координаты! ")
                continue

            x, y = cords

            if not (x.isdigit()) or not (y.isdigit()):
                print(" Введите числа! ")
                continue

            x, y = int(x), int(y)

            return Dot(x - 1, y - 1)