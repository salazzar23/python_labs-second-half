"""
Точка входа в приложение
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import PatientApp
from cli import PatientCLI
from storage import save, load
from collection import PatientCollection


def main():
    """Главная функция."""
    print("\n   Загрузка данных...")
    
    patients = load()
    
    collection = PatientCollection()
    for p in patients:
        collection.add(p)
    
    app = PatientApp(collection)
    cli = PatientCLI(app)
    
    try:
        cli.main_menu()
    finally:
        print("\n   Сохранение данных...")
        save(app.get_collection())
        print("   Программа завершена.")


if __name__ == "__main__":
    main()