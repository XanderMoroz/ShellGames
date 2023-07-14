
class Error(Exception):
    "Общий класс исключений для игры"
    pass
class BoardOutException(Error):
    def __str__(self):
        return "Вы пытаетесь выстрелить за доску!"
    pass
class BusyDotException(Error):
    def __str__(self):
        return "Эта клетка уже занята. Выберите другую."
    pass
class BoardWrongShipException(Error):
    pass
