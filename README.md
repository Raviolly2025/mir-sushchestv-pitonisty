# Мир существ · Питонисты

Проект курса «Вайбкодинг»: свой мир существ → данные → движок боя → сайт на Flask → публикация.

## Начать (один раз)
1. Вверху справа: **Use this template → Create a new repository**.
2. Имя: `mir-sushchestv`, видимость **Public** → **Create repository**.
3. В новом репозитории: **Settings → Pages → Source: GitHub Actions**.
4. **Code → Codespaces → Create codespace on main**. Подожди 1–2 минуты.
5. Ссылку на свой репозиторий (адрес из строки браузера, без слова codespaces) отправь на платформу.

## Как работать в Codespace
- Запустить файл: открой его и нажми **▶** вверху справа.
- Сайт: открой `app.py` → **▶** → вкладка **Ports** → порт 5000 → значок глобуса. Остановить: **Ctrl+C** в терминале.
- **Сохранить работу**: слева **Source Control** → напиши, что сделал → **Commit** → **Sync Changes**. Делай это в конце каждого урока!
- Codespace засыпает через 30 минут без действий — просто открой его снова: Code → Codespaces.

## Этапы
| Этап | Файлы | Проверка |
|---|---|---|
| 1. Данные мира | creatures.py | test_creatures.py |
| 2. Движок боя | battle.py, duel.py | test_battle.py |
| 3. Сайт | app.py, index/creature/battle.html, storage.py | test_site.py |

Шаги каждого этапа — в задании на платформе.
После каждого **Sync Changes** GitHub сам проверяет этапы (вкладка **Actions**: ✅ / ❌) и публикует сайт: `https://<твой-ник>.github.io/mir-sushchestv/`.
