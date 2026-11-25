# Пробный бой двух существ (первые два в CREATURES). Файл готовый — прочитай его
# и предскажи, кто победит, ДО запуска. Потом нажми ▶.
# Вопрос: где здесь используются твои функции? Что будет, если first_attacker ошибается?

from creatures import CREATURES
from battle import first_attacker, attack

a = CREATURES[0]
b = CREATURES[1]
print("Бой:", a, "против", b)

attacker = first_attacker(a, b)
defender = b if attacker is a else a
turn = 1
while a.is_alive() and b.is_alive() and turn <= 50:
    move = attacker.moves[0]          # пока всегда первый приём; выбор приёма — на этапе с ботом
    print(str(turn) + ".", attack(attacker, defender, move))
    attacker, defender = defender, attacker
    turn += 1

winner = a if a.is_alive() else b
print("Победитель:", winner.name)
