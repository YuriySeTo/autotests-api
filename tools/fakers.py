import time


def get_random_email() -> str:
    """
    Возвращает случайный email.

    :return: Строка с email.
    """
    return f"test.{time.time()}@example.com"