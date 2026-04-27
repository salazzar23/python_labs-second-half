"""
Демонстрация работы иерархии классов для ЛР-3.
Показывает все реализованные функции для оценок 3, 4 и 5.
"""

from datetime import datetime, timedelta
from base import Patient
from models import Inpatient, Outpatient
from collection import PatientCollection  # Из ЛР-2


def create_sample_patients():
    """Создание тестовых пациентов разных типов."""
    
    today = datetime.now()
    tomorrow = today + timedelta(days=1)
    next_week = today + timedelta(days=7)
    yesterday = today - timedelta(days=1)
    two_days_ago = today - timedelta(days=2)
    
    patients = [
        # Базовый пациент
        Patient("P001", "Иванов Иван", 45, "Гипертония", yesterday, "Кардиолог"),
        
        # Стационарные пациенты
        Inpatient("P002", "Петрова Мария", 68, "Инфаркт", two_days_ago, 
                 "Кардиолог", "301", two_days_ago, next_week),
        Inpatient("P003", "Сидоров Алексей", 72, "Инсульт", yesterday,
                 "Невролог", "405", yesterday, today + timedelta(days=10)),
        
        # Амбулаторные пациенты
        Outpatient("P004", "Кузнецова Елена", 35, "Гастрит", yesterday,
                  "Гастроэнтеролог", tomorrow, False),
        Outpatient("P005", "Смирнов Дмитрий", 58, "Сахарный диабет", two_days_ago,
                  "Эндокринолог", next_week, True),
    ]
    
    return patients


def demo_inheritance():
    """Демонстрация наследования (оценка 3)."""
    print("\n" + "="*70)
    print("ДЕМОНСТРАЦИЯ ОЦЕНКИ 3: Наследование")
    print("="*70)
    
    print("\n--- Создание объектов разных типов ---")
    
    # Базовый класс
    p1 = Patient("P001", "Тестовый", 30, "Тест", datetime.now(), "Терапевт")
    print(f"Базовый: {p1}")
    
    # Стационарный пациент
    p2 = Inpatient("P002", "Стационарный Тест", 50, "Пневмония", datetime.now(),
                   "Терапевт", "101", datetime.now(), datetime.now() + timedelta(days=5))
    print(f"\nСтационарный: {p2}")
    
    # Амбулаторный пациент
    p3 = Outpatient("P003", "Амбулаторный Тест", 40, "Бронхит", datetime.now(),
                    "Терапевт", datetime.now() + timedelta(days=3), False)
    print(f"\nАмбулаторный: {p3}")
    
    print("\n--- Использование методов дочерних классов ---")
    
    # Методы Inpatient
    print(f"\nInpatient методы:")
    print(f"  Дней в стационаре: {p2.get_hospitalization_days()}")
    p2.discharge()
    
    # Методы Outpatient
    print(f"\nOutpatient методы:")
    p3.register_visit()
    p3.reschedule_appointment(datetime.now() + timedelta(days=10))


def demo_polymorphism():
    """Демонстрация полиморфизма (оценка 4)."""
    print("\n" + "="*70)
    print("ДЕМОНСТРАЦИЯ ОЦЕНКИ 4: Полиморфизм")
    print("="*70)
    
    patients = create_sample_patients()
    
    print("\n--- Полиморфное поведение метода get_treatment_cost() ---")
    for patient in patients:
        cost = patient.get_treatment_cost()
        print(f"  {patient.name} ({patient.get_patient_type()}): {cost} руб.")
    
    print("\n--- Проверка типов через isinstance() ---")
    for patient in patients:
        if isinstance(patient, Inpatient):
            print(f"  {patient.name} - СТАЦИОНАРНЫЙ пациент, палата {patient.ward_number}")
        elif isinstance(patient, Outpatient):
            print(f"  {patient.name} - АМБУЛАТОРНЫЙ пациент, визитов: {patient.visit_count}")
        else:
            print(f"  {patient.name} - БАЗОВЫЙ пациент")
    
    print("\n--- Разное поведение метода display_info() ---")
    for patient in patients:
        print(f"  {patient.display_info()}")


def demo_collection_integration():
    """Демонстрация интеграции с коллекцией из ЛР-2 (оценка 4 и 5)."""
    print("\n" + "="*70)
    print("ДЕМОНСТРАЦИЯ ОЦЕНКИ 4-5: Интеграция с коллекцией")
    print("="*70)
    
    # Создаём коллекцию
    collection = PatientCollection()
    patients = create_sample_patients()
    
    print("\n--- Добавление разных типов пациентов в коллекцию ---")
    for patient in patients:
        collection.add(patient)
    
    print(f"\nВсего пациентов в коллекции: {len(collection)}")
    
    print("\n--- Все пациенты в коллекции ---")
    collection.print_all()
    
    print("\n--- Фильтрация по типу (Inpatient) ---")
    inpatients = [p for p in collection if isinstance(p, Inpatient)]
    for p in inpatients:
        print(f"  {p.name} - Стационар, палата {p.ward_number}")
    
    print("\n--- Фильтрация по типу (Outpatient) ---")
    outpatients = [p for p in collection if isinstance(p, Outpatient)]
    for p in outpatients:
        print(f"  {p.name} - Амбулаторно, визитов: {p.visit_count}")


def demo_scenarios():
    """Демонстрация сценариев использования (оценка 5)."""
    print("\n" + "="*70)
    print("СЦЕНАРИИ ИСПОЛЬЗОВАНИЯ (оценка 5)")
    print("="*70)
    
    # СЦЕНАРИЙ 1: Расчёт стоимости лечения для всех пациентов
    print("\n[СЦЕНАРИЙ 1] Расчёт стоимости лечения")
    print("-" * 50)
    
    patients = create_sample_patients()
    total_cost = 0
    
    for patient in patients:
        cost = patient.get_treatment_cost()
        total_cost += cost
        print(f"  {patient.name}: {cost} руб. ({patient.get_patient_type()})")
    
    print(f"\n  Общая стоимость лечения: {total_cost} руб.")
    
    # СЦЕНАРИЙ 2: Управление стационарными пациентами
    print("\n[СЦЕНАРИЙ 2] Управление стационарными пациентами")
    print("-" * 50)
    
    inpatients = [p for p in patients if isinstance(p, Inpatient)]
    
    for p in inpatients:
        days = p.get_hospitalization_days()
        print(f"  {p.name} - палата {p.ward_number}, дней в стационаре: {days}")
        if p.is_senior():
            print(f"    (пожилой пациент, требует особого внимания)")
    
    # СЦЕНАРИЙ 3: Запись на приём амбулаторных пациентов
    print("\n[СЦЕНАРИЙ 3] Запись на приём амбулаторных пациентов")
    print("-" * 50)
    
    outpatients = [p for p in patients if isinstance(p, Outpatient)]
    
    for p in outpatients:
        print(f"  {p.name}:")
        print(f"    Диагноз: {p.diagnosis}")
        print(f"    Следующий приём: {p.next_appointment_date.strftime('%d.%m.%Y')}")
        if p.needs_referral_check():
            print(f"    Требуется направление к узкому специалисту")
    
    # СЦЕНАРИЙ 4: Полиморфная обработка через общий интерфейс
    print("\n[СЦЕНАРИЙ 4] Полиморфная обработка через общий интерфейс")
    print("-" * 50)
    
    # Без проверки типов! Используем общий интерфейс
    for patient in patients[:4]:  # Берём первых 4 для краткости
        print(f"  Обработка: {patient.display_info()}")
        print(f"    Тип: {patient.get_patient_type()}")
        print(f"    Срочная помощь: {'Да' if patient.needs_urgent_care() else 'Нет'}")
    
    # СЦЕНАРИЙ 5: Анализ коллекции с разными типами
    print("\n[СЦЕНАРИЙ 5] Анализ коллекции пациентов")
    print("-" * 50)
    
    collection = PatientCollection()
    for p in patients:
        collection.add(p)
    
    stats = {
        "Всего": 0,
        "Стационарных": 0,
        "Амбулаторных": 0,
        "Базовых": 0,
        "Пожилых": 0
    }
    
    for p in collection:
        stats["Всего"] += 1
        if isinstance(p, Inpatient):
            stats["Стационарных"] += 1
        elif isinstance(p, Outpatient):
            stats["Амбулаторных"] += 1
        else:
            stats["Базовых"] += 1
        if p.is_senior():
            stats["Пожилых"] += 1
    
    print("СТАТИСТИКА:")
    for key, value in stats.items():
        print(f"  {key}: {value}")


def main():
    """Главная функция демонстрации."""
    print("\n" + "="*70)
    print("ЛАБОРАТОРНАЯ РАБОТА №3 - Наследование и иерархия классов")
    print("Предметная область: Медицина")
    print("="*70)
    
    demo_inheritance()
    demo_polymorphism()
    demo_collection_integration()
    demo_scenarios()
    
    print("\n" + "="*70)
    print("Демонстрация завершена. Все функции работают корректно.")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()