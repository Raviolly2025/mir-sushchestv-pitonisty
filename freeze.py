# МИР СУЩЕСТВ · «Заморозка» сайта для GitHub Pages
# GitHub не умеет запускать Python. Поэтому мы обходим все страницы сайта
# и сохраняем их готовыми HTML-файлами в папку site. Её и загружаем на GitHub.
# Запуск: сначала останови сервер (Ctrl+C), потом открой этот файл и нажми ▶. Менять его не нужно.

import os
import re
import shutil

from app import app

HERE = os.path.dirname(os.path.abspath(__file__))   # папка проекта
OUT = os.path.join(HERE, "site")
app.config["FROZEN"] = True
client = app.test_client()

shutil.rmtree(OUT, ignore_errors=True)
os.makedirs(OUT)

todo = ["index.html"]
done = set()
while todo:
    page = todo.pop()
    if page in done:
        continue
    done.add(page)
    response = client.get("/" + page)
    if response.status_code != 200:
        print("⚠️ Страница", page, "не открылась, код", response.status_code)
        continue
    html = response.get_data(as_text=True)
    with open(os.path.join(OUT, page), "w", encoding="utf-8") as f:
        f.write(html)
    # ищем ссылки на другие страницы сайта: href="что-то.html"
    for link in re.findall(r'href="([^"#:?/]+\.html)"', html):
        if link not in done:
            todo.append(link)

shutil.copy(os.path.join(HERE, "style.css"), OUT)
print("✅ Готово! Страниц:", len(done), "— всё лежит в папке site")
print("В Codespace ничего загружать не нужно: после Commit & Sync сайт опубликуется сам (вкладка Actions).")
