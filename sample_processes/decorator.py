from typing import Callable

ACTIONS: dict[str, Callable] = {}


def action(func: Callable | None = None):
    def wrapper(func: Callable):
        ACTIONS[func.__name__] = func
        return func

    return wrapper if func is None else wrapper(func)
