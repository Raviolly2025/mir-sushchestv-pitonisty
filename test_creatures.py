# ПРОВЕРКА ЭТАПА 3 (трек «Питонисты»)
# Запуск: открой этот файл и нажми ▶ вверху справа.
# Файл не меняй. Прочитай его: тесты — это тоже спецификация.

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


def raises_value_error(make):
    """True, если вызов make() выбрасывает ValueError."""
    try:
        make()
    except ValueError:
        return True
    except Exception:
        return False
    return False


print("Проверяю creatures.py...\n")
try:
    from creatures import Creature, CREATURES, ELEMENTS, BEATS, LIMITS, STAT_BUDGET
except Exception as error:
    print("❌ Файл creatures.py не запускается:", type(error).__name__, "-", error)
    raise SystemExit

E = ELEMENTS[0]
GOOD_MOVES = [{"name": "Удар", "power": 1.0}]


def make(**changes):
    data = dict(name="Тест", element=E, hp=30, attack=10, defense=5, speed=5, moves=GOOD_MOVES)
    data.update(changes)
    return Creature(**data)


print("Стихии:")
check(3 <= len(ELEMENTS) <= 5, "от 3 до 5 стихий")
check(set(BEATS.keys()) == set(ELEMENTS), "в BEATS описана каждая стихия")
all_beaten = set()
for element, victims in BEATS.items():
    check(len(victims) >= 1 and all(v in ELEMENTS and v != element for v in victims),
          element + " побеждает хотя бы одну другую стихию")
    all_beaten.update(victims)
check(all_beaten == set(ELEMENTS), "каждая стихия кому-то проигрывает")

print("\nСоздание существа (основные проверки):")
try:
    ok = make()
    check(True, "правильное существо создаётся без ошибок")
except Exception as error:
    ok = None
    check(False, "правильное существо создаётся без ошибок (" + str(error) + ")")

check(raises_value_error(lambda: make(name="")), "пустое имя → ValueError (образец уже в коде)")
check(raises_value_error(lambda: make(element="кетчуп")), "неизвестная стихия → ValueError (образец уже в коде)")
check(raises_value_error(lambda: make(hp=999)), "здоровье 999 → ValueError")
check(raises_value_error(lambda: make(speed=0)), "скорость 0 → ValueError")
check(raises_value_error(lambda: make(attack=20, defense=10, speed=10)), "превышен бюджет характеристик → ValueError")
check(raises_value_error(lambda: make(moves=[])), "нет приёмов → ValueError")

print("\nЗдоровье:")
if ok is not None:
    check(ok.is_alive() is True, "новое существо живо")
    got = ok.take_damage(7)
    check(ok.hp == 23 and got == 7, "урон 7: здоровье 30 → 23, вернулось 7")
    got = ok.take_damage(100)
    check(ok.hp == 0, "здоровье не уходит ниже 0")
    check(got == 23, "вернулся настоящий урон (23, а не 100)")
    check(ok.is_alive() is False, "при 0 здоровья существо не живо")

print("\nТвой мир:")
check(len(CREATURES) >= 4, "минимум 4 существа")
check(len(set(c.element for c in CREATURES)) >= 2, "минимум 2 разные стихии")
check(len(set(c.name for c in CREATURES)) == len(CREATURES), "имена не повторяются")

print("\nЧЕЛЛЕНДЖ (по желанию):")
bonus_ok = 0
for cond, what in [
    (raises_value_error(lambda: make(hp="30")), "здоровье строкой \"30\" → ValueError (подсказка: isinstance)"),
    (raises_value_error(lambda: make(moves=[{"name": "Супер", "power": 10}])), "приём с силой 10 → ValueError"),
    (raises_value_error(lambda: make(moves=[{"name": "Без силы"}])), "приём без power → ValueError"),
]:
    print("  ⭐" if cond else "  ·", what)
    bonus_ok += 1 if cond else 0
print("  Челлендж:", bonus_ok, "из 3")

print("\nИтог (основные):", passed, "пройдено,", failed, "не пройдено.")
if failed == 0:
    print("🎉 Основное готово! Отметь задание выполненным. Хочешь больше — добей челлендж.")
else:
    print("Исправь ❌ и запусти снова. Сначала попробуй сам, потом спроси AI «объясни, почему не проходит».")
