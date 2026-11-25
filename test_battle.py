# ПРОВЕРКА ЭТАПА 4 · ДВИЖОК БОЯ (трек «Питонисты»)
# Запуск: открой этот файл и нажми ▶ вверху справа.
# Тесты подстраиваются под ТВОЮ систему стихий из creatures.py.

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


def safe(function, *args):
    try:
        return function(*args)
    except Exception as error:
        return "ошибка: " + type(error).__name__ + " " + str(error)


print("Проверяю battle.py...\n")
try:
    from creatures import Creature, BEATS, ELEMENTS
    from battle import element_multiplier, calc_damage, first_attacker, attack
except Exception as error:
    print("❌ Не удалось загрузить файлы:", type(error).__name__, "-", error)
    raise SystemExit

# Находим в твоём мире пару «победитель → проигравший» и нейтральную пару
winner_el, loser_el = None, None
for el, victims in BEATS.items():
    if victims:
        winner_el, loser_el = el, victims[0]
        break
neutral = None
for x in ELEMENTS:
    for y in ELEMENTS:
        if x != y and y not in BEATS[x] and x not in BEATS[y]:
            neutral = (x, y)
            break
    if neutral:
        break

MOVE = {"name": "Удар", "power": 1.0}
STRONG = {"name": "Вспышка", "power": 1.5}


def make(name, element, hp=40, attack_=12, defense=4, speed=5):
    return Creature(name, element, hp, attack_, defense, speed, [MOVE])


print("[САМ] Множитель стихии (твой мир: " + winner_el + " побеждает " + loser_el + "):")
check(safe(element_multiplier, winner_el, loser_el) == 2.0, winner_el + " против " + loser_el + " → 2.0")
check(safe(element_multiplier, loser_el, winner_el) == 0.5, loser_el + " против " + winner_el + " → 0.5")
check(safe(element_multiplier, winner_el, winner_el) == 1.0, "одинаковые стихии → 1.0")
if neutral:
    check(safe(element_multiplier, neutral[0], neutral[1]) == 1.0, "нейтральная пара " + str(neutral) + " → 1.0")

print("\n[САМ] Урон:")
a = make("Атакующий", winner_el, attack_=12)
d = make("Защитник", loser_el, defense=8)
check(safe(calc_damage, a, d, MOVE) == 16, "12 × 1.0 × 2.0 − 8 = 16")
check(safe(calc_damage, a, d, STRONG) == 28, "12 × 1.5 × 2.0 − 8 = 28")
weak = make("Слабый", loser_el, attack_=9)
strong_def = make("Танк", winner_el, defense=10)
check(safe(calc_damage, weak, strong_def, MOVE) == 1, "9 × 1.0 × 0.5 = 4.5 → 4, 4 − 10 < 1 → урон 1")
result = safe(calc_damage, a, d, STRONG)
check(isinstance(result, int), "урон — целое число (int), а не дробное")

print("\n[С AI] Кто ходит первым:")
fast = make("Быстрый", winner_el, speed=9)
slow = make("Медленный", winner_el, speed=3)
check(safe(first_attacker, slow, fast) is fast, "ходит тот, у кого выше скорость")
x = make("Икс", winner_el, hp=50, speed=5)
y = make("Игрек", winner_el, hp=30, speed=5)
check(safe(first_attacker, y, x) is x, "при равной скорости — у кого больше здоровья")
p = make("Пэ", winner_el, hp=30, speed=5)
q = make("Ку", winner_el, hp=30, speed=5)
check(safe(first_attacker, p, q) is p, "при полном равенстве — первый аргумент")

print("\n[С AI] Атака:")
a = make("Искра", winner_el, attack_=12)
d = make("Лист", loser_el, hp=40, defense=8)
line = safe(attack, a, d, MOVE)
check(d.hp == 24, "после атаки здоровье защитника 40 − 16 = 24 (у тебя: " + str(d.hp) + ")")
check(isinstance(line, str) and "Искра" in line and "Лист" in line and "-16" in line,
      "строка лога содержит имена и -16 (у тебя: " + repr(line) + ")")
check(isinstance(line, str) and "суперэффективно" in line, "в логе есть «суперэффективно»")
line2 = safe(attack, d, a, MOVE)
check(isinstance(line2, str) and "неэффективно" in line2, "обратная атака помечена «неэффективно»")

import inspect
try:
    source_lines = inspect.getsource(attack).splitlines()
    comments = [l for l in source_lines if l.strip().startswith("#")]
except Exception:
    comments = []
check(len(comments) >= 3, "в attack() минимум 3 твоих комментария (сейчас: " + str(len(comments)) + ") — объясни код своими словами")

print("\nИтог:", passed, "пройдено,", failed, "не пройдено.")
if failed == 0:
    print("🎉 Движок готов. Открой duel.py и нажми ▶ — но сначала предскажи победителя!")
else:
    print("Сначала найди ошибку сам: в строке с ❌ написано, что должно получиться, — найди функцию, которая за это отвечает.")
