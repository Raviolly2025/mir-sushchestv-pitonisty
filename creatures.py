# МИР СУЩЕСТВ · Класс существа (питонисты)
# Шаги — в задании на платформе. Запуск файла — кнопка ▶ вверху справа.
# Тесты = задание: открой test_creatures.py, нажми ▶ и смотри, что красное.
# [САМ] — пишешь сам, AI только объясняет. [С AI] — AI пишет по твоему описанию, ты проверяешь.

ELEMENTS = ["fire", "water", "nature"]

BEATS = {
    "fire": ["nature"],
    "nature": ["water"],
    "water": ["fire"],
}

LIMITS = {
    "hp": (20, 60),
    "attack": (5, 20),
    "defense": (0, 10),
    "speed": (1, 10),
}
STAT_BUDGET = 30
MAX_NAME_LENGTH = 20
POWER_LIMITS = (0.5, 2.0)


class Creature:
    def __init__(self, name, element, hp, attack, defense, speed, moves):
        # --- Проверка 1 (готово, это образец) ---
        if name == "" or len(name) > MAX_NAME_LENGTH:
            raise ValueError("Имя должно быть от 1 до 20 символов")

        # --- Проверка 2 (готово, это образец) ---
        if element not in ELEMENTS:
            raise ValueError("Неизвестная стихия: " + str(element))

        # --- [САМ] Проверка 3: характеристики в допустимых пределах ---
        # TODO: для hp, attack, defense, speed проверь, что значение в пределах LIMITS.
        # Подсказка: можно сложить характеристики в словарь и пройти циклом:
        #   stats = {"hp": hp, "attack": attack, "defense": defense, "speed": speed}
        #   for stat_name in stats:
        #       low, high = LIMITS[stat_name]
        #       ...

        # --- [САМ] Проверка 4: бюджет ---
        # TODO: attack + defense + speed не больше STAT_BUDGET

        # --- [С AI] Проверка 5: приёмы ---
        # TODO: приёмов 1 или 2 (len(moves))

        self.name = name
        self.element = element
        self.max_hp = hp
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.moves = moves

    # [САМ]
    def is_alive(self):
        """TODO: вернуть True, если здоровье больше нуля, иначе False."""
        pass

    # [САМ]
    def take_damage(self, amount):
        """
        TODO: уменьшить здоровье на amount, но не ниже 0.
        Вернуть, сколько урона получено на самом деле:
        при здоровье 5 и уроне 9 вернуть 5.
        """
        pass

    def __repr__(self):
        return "<" + self.name + " (" + self.element + ") " + str(self.hp) + "/" + str(self.max_hp) + ">"


# TODO: минимум 4 существа, хотя бы 2 разные стихии
CREATURES = [
    Creature("Искрохвост", "fire", 40, 12, 4, 7,
             [{"name": "Вспышка", "power": 1.5}, {"name": "Укус", "power": 1.0}]),
]


if __name__ == "__main__":
    for creature in CREATURES:
        print(creature, "приёмы:", [m["name"] for m in creature.moves])
