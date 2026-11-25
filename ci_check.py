# Запускает тест и сообщает GitHub, прошёл ли он (используется автопроверкой). Менять не нужно.
import runpy
import sys

try:
    result = runpy.run_path(sys.argv[1], run_name="__main__")
    failed = result.get("failed", 1)
except SystemExit:
    failed = 1
sys.exit(1 if failed else 0)
