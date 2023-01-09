def get_number(mistake):
    if mistake == 0:
        return 'Поздравляю!, это лучший результат!'
    elif mistake == 1:
        return 'Вы сделали одну ошибку. Отличный результат :)'
    elif mistake >= 2 and mistake < 5:
        return f'Вы сделали {mistake} ошибки'
    elif mistake >= 5 and mistake <= 20:
        return f'Вы сделали {mistake} ошибoк'
    else:
        return f'Вы сделали больше 20 ошибок :('
