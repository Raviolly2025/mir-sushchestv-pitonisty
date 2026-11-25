# МИР СУЩЕСТВ · Хранение истории боёв в файле history.json
# Работает, только когда запущен сервер (app.py). На GitHub-версии истории нет.

import json
import os

FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "history.json")
MAX_BATTLES = 20          # храним только последние бои
MAX_NAME_LENGTH = 20


# [САМ] шаг 5
def load_history():
    """
    Прочитать историю из FILE и вернуть список боёв (словари first, second, winner).
    Файл может не существовать, быть сломанным или подменённым — тогда не падать:
    - нет файла или не JSON → вернуть [];
    - берём только словари, где first, second, winner — строки не длиннее MAX_NAME_LENGTH;
    - вернуть последние MAX_BATTLES.
    """
    return []


# [САМ] шаг 5
def add_battle(first, second, winner):
    """Добавить бой в историю и сохранить в FILE (json, ensure_ascii=False). Хранить не больше MAX_BATTLES."""
    pass
