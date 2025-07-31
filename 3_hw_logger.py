import datetime
import functools


def logger(file_path):
    def __logger(old_function):
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
                        f"{current_time}: Функция '{old_function.__name__}' "
                        f"вызвана с аргументами {args}, {kwargs}."
                        f"Результат: {result}\\n")
                    return result
            except Exception as e:
                with open(file_path, mode='a', encoding='utf-8') as log_file:
                    log_file.write(
                        f"{current_time}:"
                        f"Ошибка при вызове функции '{old_function.__name__}'."
                        f"с аргуентами {args}, {kwargs}. "
                        f"Ошибка: {str(e)}\\n")
                    raise

        return new_function

    return __logger


@logger('app_logs.txt')
def discriminant(a, b, c):
    return b ** 2 - 4 * a * c


@logger('app_logs.txt')
def solution(a, b, c):
    d = discriminant(a, b, c)
    if d < 0:
        return "корней нет"
    elif d == 0:
        x = -b/(2*a)
        return x
    else:
        x1 = (-b + d ** 0.5)/(2 * a)
        x2 = (-b - d ** 0.5) / (2 * a)
        return x1, x2


if __name__ == '__main__':
    solution(1, 8, 15)     # -3.0 -5.0
    solution(1, -13, 12)   # 12.0 1.0
    solution(-4, 28, -49)  # 3.5
    solution(1, 1, 1)      # корней нет
