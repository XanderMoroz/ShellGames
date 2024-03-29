print("*" * 10, " Игра Крестики-нолики для двух игроков ", "*" * 10)

list_for_xo_board = ["7", "8", "9", "4", "5", "6", "1", "2", "3"]
"""Создаем одномерный список из 9 игровых полей"""

def board_building(board_list):
    """
    Выводит по 3 элемента списка на трех строках - чтобы получилось игровое поле 3*3.
    :Аргумент: board_list; - список игровых полей
    :Возвращает: по 3 элемента списка за одну итерацию
    """
    print(" " + "~~~ " * 3)
    for elem in range(3):
        print("|", board_list[0 + elem * 3], "|", board_list[1 + elem * 3], "|", board_list[2 + elem * 3], "|")
        print(" " + "~~~ " * 3)

def input_checker(symbol):
    """
    1) Проверяет корректность значения, введенного игроком. Значение должно быть числом в диапазоне от 1 до 9.
    2) После успешной проверки помещает аргумент на одно из 9 полей, при условии, что это поле еще не занято.
    :Аргумент: symbol; - Крестик("Х"), либо Нолик("O").
    :Возвращает: обновленный список игровых полей с новым крестиком или ноликом.
    """
    sucsessful_check = False
    while sucsessful_check is not True:
        player_choice = input("Выберите номер клетки в которую хотите поставить " + symbol + "? \n")
        try:
            player_choice = int(player_choice)
        except:
            print("Требуется числовое значение! Попробуйте еще раз:")
            continue
        if 0 < player_choice <= 9:
            if player_choice < 4:
                player_choice += 6
            elif player_choice > 6:
                player_choice -= 6
            if (str(list_for_xo_board[player_choice - 1]) not in "XO"):
                list_for_xo_board[player_choice - 1] = symbol
                sucsessful_check = True
            else:
                print("Вы не можете поставить" + symbol + "Эта клетка уже занята!")
        else:
            print("Некорректный ввод. Введите число в диапазоне от 1 до 9.")

def win_checker():
    """
    1) Создает список комбинаций индексов игрового поля, означающих победу игрока.
    2) Проверяет заполнение выигрышных индексов игрового поля, одним из символов (крестик или нолик).
    :Возвращает: либо символ победителя (Х или О), либо False.
    """
    win_combinations = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))
    for comb in win_combinations:
        if list_for_xo_board[comb[0]] == list_for_xo_board[comb[1]] == list_for_xo_board[comb[2]]:
            return list_for_xo_board[comb[0]]
    return False

def game_cicler(board_list):
    """
    1) Создает счетчик ходов в партии  комбинаций индексов игрового поля, означающих победу игрока.
    2) До тех пор пока не определится победитель: выполняет ход, записывает значение.
    3) С пятого хода начинает проверять состояние поля с выигрышными комбинациями пока не определит победителя.
    :Аргумент: board_list; - список игровых полей
    :Возвращает: строку "В этот раз победил игрок ставивший", winner, "Поздравляем!"
    """
    move_count = 0
    got_winner = False
    while got_winner is not True:
        board_building(board_list)
        if move_count % 2 == 0:
            input_checker("X")
        else:
            input_checker("O")
        move_count += 1
        if move_count > 4:
            winner = win_checker()
            if winner:
                board_building(board_list)
                print("В этот раз победил игрок ставивший", winner, "Поздравляем!")
                got_winner = True
                break
        if move_count == 9:
            print("А это Ничья!")
            break

game_cicler(list_for_xo_board)
