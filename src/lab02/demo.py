from datetime import datetime, timedelta
from model import Patient
from collection import PatientCollection

def main():
    print("="*60)
    print("Демонстрация работы коллекции пациентов")
    print("="*60)
    
    # Создаём коллекцию
    collection = PatientCollection()
    print("\n1. Создана пустая коллекция")
    
    # Создаём пациентов
    today = datetime.now()
    p1 = Patient("P001", "Иванов Иван", 45, "Гипертония", today, "Кардиолог")
    p2 = Patient("P002", "Петрова Мария", 68, "Артрит", today, "Ревматолог")
    p3 = Patient("P003", "Сидоров Алексей", 72, "Инфаркт", today, "Кардиолог")
    
    # Добавляем
    print("\n2. Добавление пациентов:")
    collection.add(p1)
    collection.add(p2)
    collection.add(p3)
    
    # Показываем всех
    print("\n3. Все пациенты:")
    collection.print_all()
    
    # Поиск
    print("\n4. Поиск по ID P002:")
    collection.find_by_id("P002")
    
    # Длина коллекции
    print(f"\n5. Количество пациентов: {len(collection)}")
    
    # Итерация
    print("\n6. Перебор через for:")
    for patient in collection:
        print(f"   - {patient.name}")
    
    # Индексация
    print(f"\n7. Первый пациент: {collection[0].name}")
    print(f"   Последний пациент: {collection[-1].name}")
    
    # Удаление
    print("\n8. Удаление второго пациента:")
    collection.remove(p2)
    collection.print_all()
    
    print("\n" + "="*60)
    print("Демонстрация завершена!")
    print("="*60)

if __name__ == "__main__":
    main()