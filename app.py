# МИР СУЩЕСТВ · Сайт (сервер на Flask)
# Запуск: нажми ▶ — откроется браузер с твоим сайтом. Остановить сервер: Ctrl+C в терминале.
# Адреса страниц заканчиваются на .html — так сайт потом можно «заморозить» для GitHub (freeze.py).
# Все файлы лежат в одной папке: шаблоны страниц (*.html) и стиль style.css — рядом с app.py.

import os
import webbrowser

from flask import Flask, render_template, abort, send_from_directory

from creatures import CREATURES
from battle import fight
import storage

HERE = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, template_folder=HERE, static_folder=None)
app.config["FROZEN"] = False   # True — когда freeze.py делает «фотографию» сайта для GitHub


def get_creature(number):
    """Существо по номеру или страница «не найдено» (404)."""
    if 0 <= number < len(CREATURES):
        return CREATURES[number]
    abort(404)


@app.route("/")
@app.route("/index.html")
def index():
    pairs = []
    for a in range(len(CREATURES)):
        for b in range(len(CREATURES)):
            if a != b:
                pairs.append((a, b))
    return render_template("index.html", creatures=CREATURES, pairs=pairs)


@app.route("/creature-<int:number>.html")
def creature_page(number):
    return render_template("creature.html", creature=get_creature(number), number=number)


@app.route("/battle-<int:a>-<int:b>.html")
def battle_page(a, b):
    """
    [САМ] шаг 4. Страница боя существа номер a против существа номер b.
    1) найди обоих бойцов (get_creature); 2) проведи бой: fight → лог и победитель;
    3) если сайт НЕ заморожен (app.config["FROZEN"]) — сохрани бой: storage.add_battle(имя, имя, имя победителя);
    4) верни шаблон battle.html с переменными first, second, log, winner.
    """
    pass


@app.route("/style.css")
def style():
    return send_from_directory(HERE, "style.css")


@app.route("/history.html")
def history_page():
    """
    [САМ] шаг 5. Страница истории. На замороженном сайте (FROZEN) истории нет — передай пустой список.
    Иначе — storage.load_history(). Шаблон history.html, переменная battles.
    """
    pass


if __name__ == "__main__":
    if os.environ.get("WERKZEUG_RUN_MAIN") != "true":   # чтобы браузер не открылся дважды
        webbrowser.open("http://127.0.0.1:5000")
    app.run(debug=True)
