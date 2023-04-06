# 1. Доработать декоратор logger в коде ниже.

# Должен получиться декоратор, который записывает в файл 'main.log'
# дату и время вызова функции,
# имя функции, аргументы, с которыми вызвалась, возвращаемое значение.

#  Функция test_1 в коде ниже также должна отработать без ошибок.


# 2. Доработать параметризованный декоратор logger в коде ниже.
# Должен получиться декоратор, который записывает в файл:
# дату и время вызова функции, имя функции,
# аргументы, с которыми вызвалась, и возвращаемое значение.

# Путь к файлу должен передаваться в аргументах декоратора.
# Функция test_2 в коде ниже также должна отработать без ошибок.


# 3. Применить написанный логгер к приложению из любого предыдущего д/з


import os
from itertools import chain


def logger(path):
    def __logger(old_func):
        from datetime import datetime

        def new_func(*args, **kwargs):
            list_value = []

            call_time = str(datetime.now())
            name_func = old_func.__name__
            old_func(*args, **kwargs)
            arguments = [args, kwargs]

            result = old_func(*args, **kwargs)
            list_value.append(name_func)
            list_value.append(call_time)
            list_value.append(arguments)
            list_value.append(result)
            with open(path, 'a') as f:
                for i in list_value:
                    f.write(str(i) + '\n')
                f.write('\n')
            return old_func(*args, **kwargs)

        return new_func

    return __logger


def test_1():
    path = 'main.log'
    if os.path.exists(path):
        os.remove(path)

    @logger(path)
    def hello_world():
        return 'Hello World'

    @logger(path)
    def summator(a, b=0):
        return a + b

    @logger(path)
    def div(a, b):
        return a / b

    assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
    result = summator(2, 2)
    assert isinstance(result, int), 'Должно вернуться целое число'
    assert result == 4, '2 + 2 = 4'
    result = div(6, 2)
    assert result == 3, '6 / 2 = 3'

    assert os.path.exists(path), 'файл main.log должен существовать'

    summator(4.3, b=2.2)
    summator(a=0, b=0)

    with open(path) as log_file:
        log_file_content = log_file.read()

    assert 'summator' in log_file_content, 'должно записаться имя функции'
    for item in (4.3, 2.2, 6.5):
        assert str(item) in log_file_content, f'{item} должен быть записан в файл'


def test_2():
    paths = ('log_1.log', 'log_2.log', 'log_3.log')

    for path in paths:
        if os.path.exists(path):
            os.remove(path)

        @logger(path)
        def hello_world():
            return 'Hello World'

        @logger(path)
        def summator(a, b=0):
            return a + b

        @logger(path)
        def div(a, b):
            return a / b

        assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
        result = summator(2, 2)
        assert isinstance(result, int), 'Должно вернуться целое число'
        assert result == 4, '2 + 2 = 4'
        result = div(6, 2)
        assert result == 3, '6 / 2 = 3'
        summator(4.3, b=2.2)

    for path in paths:

        assert os.path.exists(path), f'файл {path} должен существовать'

        with open(path) as log_file:
            log_file_content = log_file.read()

        assert 'summator' in log_file_content, 'должно записаться имя функции'

        for item in (4.3, 2.2, 6.5):
            assert str(item) in log_file_content, f'{item} должен быть записан в файл'
            

@logger('class.log')
class FlatIterator:

    def __init__(self, list_of_list):
        self.list_of_list = list_of_list
        self.counter = -1
        self.list_of_list = list(chain.from_iterable(list_of_list))

    def __iter__(self):
        return self

    def __next__(self):
        if self.counter + 1 >= len(self.list_of_list):
            raise StopIteration()
        else:
            self.counter += 1
            return self.list_of_list[self.counter]
        
        
def test_3():
    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]

    for flat_iterator_item, check_item in zip(
            FlatIterator(list_of_lists_1),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]):
        assert flat_iterator_item == check_item

    assert list(FlatIterator(list_of_lists_1)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]


if __name__ == '__main__':
    test_1()
    test_2()
    test_3()
