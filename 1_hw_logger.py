import os
import datetime
import functools


def logger(old_function):
    file_path = 'main.log'

    @functools.wraps(old_function)
    def new_function(*args, **kwargs):
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"{current_time}: {old_function.__name__} "
              f"вызвана с аргументами args={args}, kwargs={kwargs}. "
              f"Результат: {old_function(*args, **kwargs)}")
        try:
            result = old_function(*args, **kwargs)
            with open(file_path, mode='a', encoding='utf-8') as log_file:
                log_file.write(
                    f"{current_time}: Функция '{old_function.__name__}"
                    f"вызвана с аргументами {args}, {kwargs}."
                    f"Результат: {result}\\n")
            return result
        except Exception as e:
            # Если произошла ошибка
            with open(file_path, mode='a', encoding='utf-8') as log_file:
                log_file.write(
                    f"{current_time}:"
                    f"Ошибка при вызове функции '{old_function.__name__}'."
                    f"с аргуентами {args}, {kwargs}. "
                    f"Ошибка: {str(e)}\\n")
            raise

    return new_function


def test_1():

    path = 'main.log'
    if os.path.exists(path):
        os.remove(path)

    @logger
    def hello_world():
        return 'Hello World'

    @logger
    def summator(a, b=0):
        return a + b

    @logger
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


if __name__ == '__main__':
    test_1()
