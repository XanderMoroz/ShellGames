from random import randint

from ShellGames.Sea_Battle.elements.board import Board
from ShellGames.Sea_Battle.elements.dot import Dot
from ShellGames.Sea_Battle.elements.ship import Ship
from ShellGames.Sea_Battle.elements.user import User, Ai
from ShellGames.Sea_Battle.exeptions import BoardWrongShipException


class Game:
    "Базовый класс игровой сессии"

    def __init__(self, size_of_board = 6):
        self.lens_of_ships = [3, 2, 2, 1, 1, 1, 1]
        self.size = size_of_board
        player_board = self.random_board()
        ai_board = self.random_board()
        ai_board.hid = True

        self.ai = Ai(ai_board,player_board)
        self.user = User(player_board, ai_board)

    def create_board(self):
        """
        Метод осуществляет попытки расположить корабли на доске.
        :return: объект класса Board - доска с расположенными на ней кораблями.
        """
        lens_of_ships = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size = self.size)
        attempts = 0
        for elem in lens_of_ships:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), elem, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def random_board(self):
        """
        Метод генерирует случайную доску.
        :return: объект класса Board - доска с кораблями, расположенными случайным образом.
        """
        board = None
        while board is None:
            board = self.create_board()
        return board

    def greet(self):
        "Метод, который в консоли приветствует пользователя и рассказывает о формате ввода."
        print("---------------------------")
        print("  Приветствуем вас в игре  ")
        print("       'МОРСКОЙ БОЙ'       ")
        print("---------------------------")
        print("     формат ввода: x y     ")
        print("     x - номер строки      ")
        print("     y - номер столбца     ")

    def cicle(self):
        """
        Метод с самим игровым циклом. Последовательно вызываем метод move для игроков и делаем проверку,
        сколько живых кораблей осталось на досках, чтобы определить победу.
        """
        num = 0
        while True:
            print("-" * 27)
            print("Это ваша доска:")
            print(self.user.my_board)
            print("-" * 27)
            print("Доска противника:")
            print(self.ai.my_board)
            print("-" * 27)
            if num % 2 == 0:
                print("Ваш ход!")
                repeat = self.user.move()
            else:
                print("Ход противника!")
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.my_board.shooted_ship == 7:
                print("-" * 27)
                print("Вы победили!")
                break

            if self.user.my_board.shooted_ship == 7:
                print("-" * 20)
                print("Ваш противник выиграл!")
                break
            num += 1

    def start(self):
        "Метод запускающий приветствие и цикл игры"
        self.greet()
        self.cicle()