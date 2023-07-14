from random import randint


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

new_game = Game()
new_game.start()