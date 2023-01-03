from django import template

register = template.Library()


def censorword(word):
    # создаем словарь цензуры. Записываем начало слов, которые подлежат цензуре.
    # В словаре можно опустить окончания слов и приставки не более 2-х символов, для сокращения словаря
    censored = ['хуй', 'пизд', 'хуи', 'хуе', 'прихуе', 'ебал', 'ебаш', 'ебат',
                'ебан', 'заеб', 'заёб', 'ебнул']
    # проверяем вхождение бранного слова в каждое слово в тексте
    for abuse in censored:
        try:
            # если комбинация букв из словаря попалась не в начале слова, скорее всего это случайное совпадение
            if word.lower().index(abuse) > 2:
                continue  # переходим к следующему
        except ValueError:  # если в слове нет вхождений из словаря
            continue  # переходим к следующему
        else:  # если слово бранное печатаем вместо него *
            censored_word = word[0] + '*' * len(word[1:])
            return censored_word  # и возвращаем в зацензуренном виде
    return word  # если слово прошло фильтр, возвращаем его без изменений


@register.filter()
def censor(text):
    if type(text) is str:  # проверяем что text это строка
        words = text.split()  # разделяем текст на слова
        for i in range(len(words)):  # каждое слово прогоняем через цензуру
            words[i] = censorword(words[i])
    else:  # если фильтр применен не к строке
        raise AttributeError(f'Фильтр был применен к недопустимому типу данных: {type(text)}')
    return ' '.join(words)  # возвращаем текст с учетом цензуры