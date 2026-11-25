# ПРОВЕРКА САЙТА «МИР СУЩЕСТВ»
# Запуск: открой этот файл и нажми ▶ (сервер при этом можно не останавливать). Файл менять не нужно.

import os
import re
import tempfile

passed = 0
failed = 0


def check(condition, what):
    global passed, failed
    if condition:
        passed += 1
        print("  ✅", what)
    else:
        failed += 1
        print("  ❌", what)


HERE = os.path.dirname(os.path.abspath(__file__))
print("Проверяю сайт...\n")
try:
    import storage
    storage.FILE = os.path.join(tempfile.mkdtemp(), "history.json")   # тест не трогает твою историю
    from app import app
    import creatures as creatures_module
except Exception as error:
    print("❌ Сайт не запускается:", type(error).__name__, "-", error)
    print("Подсказка: открой app.py и нажми ▶ — Python покажет строку с ошибкой.")
    raise SystemExit

app.logger.disabled = True   # ошибки сервера не печатаем целиком — тест сам скажет, что не так
CREATURES = getattr(creatures_module, "CREATURES", None) or getattr(creatures_module, "creatures")
client = app.test_client()


def name_of(c):
    return c["name"] if isinstance(c, dict) else c.name


def get(url):
    try:
        r = client.get(url)
        return r.status_code, r.get_data(as_text=True)
    except Exception as error:
        return 500, "ошибка: " + type(error).__name__ + " " + str(error)


print("Шаблоны страниц (шаг 3):")
for page in ["index.html", "creature.html", "battle.html"]:
    text = open(os.path.join(HERE, page), encoding="utf-8").read()
    check("ВСТАВЬ СЮДА" not in text, page + ": вставлен шаблон от AI (заглушки больше нет)")
    check('{% extends "base.html" %}' in text or "{% extends 'base.html' %}" in text, page + ": начинается с {% extends \"base.html\" %}")
    check("|safe" not in text.replace(" ", ""), page + ": нет |safe")
    check(not re.search(r'<script[^>]+src=["\']https?://', text), page + ": нет чужих скриптов из интернета")

print("\nГлавная страница:")
code, html = get("/index.html")
check(code == 200, "открывается (код " + str(code) + ")")
check(all(name_of(c) in html for c in CREATURES), "на ней имена всех существ")
check("creature-0.html" in html, "есть ссылки на карточки (creature-0.html …)")
check("battle-0-1.html" in html, "есть ссылки на бои (battle-0-1.html …)")
check('href="/' not in html, "все ссылки без / в начале (иначе сломаются на GitHub)")

print("\nКарточка существа (шаг 4):")
code, html = get("/creature-0.html")
check(code == 200, "creature-0.html открывается (код " + str(code) + ")")
check(name_of(CREATURES[0]) in html, "на карточке имя существа")

print("\nСтраница боя (шаг 4):")
code, html = get("/battle-0-1.html")
check(code == 200, "battle-0-1.html открывается (код " + str(code) + ")")
check(name_of(CREATURES[0]) in html and name_of(CREATURES[1]) in html, "на странице имена обоих бойцов")
check(html.count("→") >= 2, "есть лог боя (строки с →)")
check("Победитель" in html or "победитель" in html, "показан победитель")

print("\nИстория боёв (шаг 5):")
get("/battle-1-0.html")
code, html = get("/history.html")
check(code == 200, "history.html открывается")
check(name_of(CREATURES[1]) in html and "⚔" in html, "бой, который только что прошёл, попал в историю")

print("\nБезопасность (шаг 6):")
evil = "<script>alert(1)</script>"
first = CREATURES[0]
old = first["name"] if isinstance(first, dict) else first.name
try:
    if isinstance(first, dict):
        first["name"] = evil
    else:
        first.name = evil
    code, html = get("/index.html")
    check(evil not in html and "&lt;script&gt;" in html, "имя с <script> показывается как текст, а не выполняется")
finally:
    if isinstance(first, dict):
        first["name"] = old
    else:
        first.name = old

print("\nfight — бой целиком (шаг 4):")
try:
    from battle import fight
    a, b = CREATURES[0], CREATURES[1]
    hp_before = (a.hp, b.hp)
    result = fight(a, b)
    ok_shape = isinstance(result, tuple) and len(result) == 2 and isinstance(result[0], list)
    check(ok_shape, "fight возвращает (список строк лога, победитель)")
    check((a.hp, b.hp) == hp_before, "существа из CREATURES после боя не изменились (бьются копии)")
    if ok_shape:
        check(result[1] in (a, b) or getattr(result[1], "name", None) in (a.name, b.name), "победитель — один из бойцов")
        check(len(result[0]) <= 50, "бой не бесконечный (не больше 50 ходов)")
    import inspect
    comments = [l for l in inspect.getsource(fight).splitlines() if l.strip().startswith("#")]
    check(len(comments) >= 3, "в fight минимум 3 твоих комментария (сейчас: " + str(len(comments)) + ")")
except Exception as error:
    check(False, "fight работает (" + type(error).__name__ + ": " + str(error) + ")")

print("\nstorage — надёжное хранение (шаг 5):")
try:
    with open(storage.FILE, "w", encoding="utf-8") as f:
        f.write("{ это не JSON")
    check(storage.load_history() == [], "сломанный history.json не роняет сайт — возвращается пустая история")
    with open(storage.FILE, "w", encoding="utf-8") as f:
        f.write('[{"first": "А", "second": "Б", "winner": "' + "Х" * 500 + '"}, "мусор", {"first": "В", "second": "Г", "winner": "В"}]')
    h = storage.load_history()
    check(len(h) == 1 and h[0]["winner"] == "В", "подозрительные записи (не словарь, имя 500 символов) отбрасываются")
    os.remove(storage.FILE)
    for i in range(25):
        storage.add_battle("А", "Б", "А")
    check(len(storage.load_history()) == 20, "хранятся только последние 20 боёв")
except Exception as error:
    check(False, "storage работает (" + type(error).__name__ + ": " + str(error) + ")")

print("\nИтог:", passed, "пройдено,", failed, "не пройдено.")
if failed == 0:
    print("🎉 Сайт готов! Останови сервер (Ctrl+C), открой freeze.py и нажми ▶.")
else:
    print("Исправь строки с ❌. Ошибка в шаблоне — сверь его с чек-листом из уровня «Карта сайта и запросы к AI».")
