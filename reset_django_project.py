import os
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 1. Удаляем базу данных
db_path = os.path.join(BASE_DIR, "db.sqlite3")
if os.path.exists(db_path):
    os.remove(db_path)
    print("✅ Удалён файл базы данных: db.sqlite3")

# 2. Удаляем миграции кроме __init__.py
print("📦 Поиск и удаление миграций...")
for root, dirs, files in os.walk(BASE_DIR):
    if "migrations" in root:
        for file in files:
            if file.endswith(".py") and file != "__init__.py":
                os.remove(os.path.join(root, file))
            elif file.endswith(".pyc"):
                os.remove(os.path.join(root, file))
print("✅ Миграции удалены.")

# 3. Удаляем .pyc файлы по всему проекту
print("🧹 Удаление .pyc файлов...")
for root, dirs, files in os.walk(BASE_DIR):
    for file in files:
        if file.endswith(".pyc"):
            os.remove(os.path.join(root, file))
print("✅ .pyc файлы удалены.")

print("\n💡 Готово! Теперь выполни:")
print("   python manage.py makemigrations")
print("   python manage.py migrate")
print("   python manage.py createsuperuser")
