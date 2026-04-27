from datetime import datetime, timedelta
from base import Patient
from models import Inpatient, Outpatient
from collection import PatientCollection


def create_test_data():
    """Создание тестовых пациентов."""
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    two_days_ago = today - timedelta(days=2)
    tomorrow = today + timedelta(days=1)
    next_week = today + timedelta(days=7)
    
    return [
        Patient("P001", "Иванов Иван", 45, "Гипертония", "Кардиолог"),
        Patient("P008", "Новиков Павел", 32, "Здоров", "Терапевт"),
        Inpatient("P002", "Петрова Мария", 68, "Инфаркт", "Кардиолог", "301", yesterday),
        Inpatient("P003", "Сидоров Алексей", 72, "Инсульт", "Невролог", "405", two_days_ago),
        Inpatient("P006", "Васильева Анна", 25, "Аппендицит", "Хирург", "210", yesterday),
        Outpatient("P004", "Кузнецова Елена", 35, "Гастрит", "Гастроэнтеролог", tomorrow),
        Outpatient("P005", "Смирнов Дмитрий", 58, "Диабет", "Эндокринолог", next_week),
        Outpatient("P007", "Михайлов Сергей", 80, "Аритмия", "Кардиолог", next_week),
    ]


def scenario_1():
    """Сценарий 1: Базовые операции."""
    print("\n" + "="*60)
    print("СЦЕНАРИЙ 1: БАЗОВЫЕ ОПЕРАЦИИ")
    print("="*60)
    
    col = PatientCollection()
    patients = create_test_data()
    
    print("\n--- 1.1 Добавление пациентов ---")
    for p in patients[:5]:
        col.add(p)
    
    print("\n--- 1.2 Вывод всех пациентов ---")
    col.print_all()
    
    print("\n--- 1.3 Удаление пациента P002 ---")
    col.remove(patients[1])
    
    print("\n--- 1.4 После удаления ---")
    col.print_all()
    
    print("\n--- 1.5 Проверка дубликатов ---")
    col.add(patients[0])
    
    print("\n--- 1.6 Проверка типа ---")
    try:
        col.add("это строка")
    except TypeError as e:
        print(f"   Ошибка: {e}")
    
    print(f"\n--- Итог: {len(col)} пациентов ---")


def scenario_2():
    """Сценарий 2: Поиск."""
    print("\n" + "="*60)
    print("СЦЕНАРИЙ 2: ПОИСК")
    print("="*60)
    
    col = PatientCollection()
    patients = create_test_data()
    
    for p in patients:
        col.add(p)
    
    print(f"\n--- 2.1 len(collection) = {len(col)} ---")
    
    print("\n--- 2.2 Поиск по ID ---")
    col.find_by_id("P004")
    col.find_by_id("P999")
    
    print("\n--- 2.3 Поиск по имени ---")
    col.find_by_name("Иван")
    col.find_by_name("Смирнов")
    
    print("\n--- 2.4 Поиск по диагнозу ---")
    col.find_by_diagnosis("инфаркт")
    col.find_by_diagnosis("диабет")
    
    print("\n--- 2.5 Итерация (for) ---")
    for i, p in enumerate(col):
        print(f"   {i+1}. {p.name} - {p.diagnosis}")
    
    print("\n--- 2.6 Проверка вхождения ---")
    print(f"   P001 в коллекции: {patients[0] in col}")
    fake = Patient("P999", "Фейк", 1, "Тест", "Врач")
    print(f"   Фейк в коллекции: {fake in col}")


def scenario_3():
    """Сценарий 3: Индексация и сортировка."""
    print("\n" + "="*60)
    print("СЦЕНАРИЙ 3: ИНДЕКСАЦИЯ И СОРТИРОВКА")
    print("="*60)
    
    col = PatientCollection()
    patients = create_test_data()
    
    for p in patients:
        col.add(p)
    
    print("\n--- 3.1 Доступ по индексу ---")
    print(f"   collection[0] = {col[0].name}")
    print(f"   collection[2] = {col[2].name}")
    print(f"   collection[-1] = {col[-1].name}")
    
    print("\n--- 3.2 Срезы ---")
    print("   collection[0:3]:")
    for p in col[0:3]:
        print(f"     - {p.name}")
    
    print("\n--- 3.3 Сортировка по возрасту (возрастание) ---")
    sorted_by_age = col.sort_by_age()
    for p in sorted_by_age:
        print(f"     - {p.name}: {p.age} лет")
    
    print("\n--- 3.4 Сортировка по возрасту (убывание) ---")
    sorted_by_age_desc = col.sort_by_age(reverse=True)
    for p in sorted_by_age_desc:
        print(f"     - {p.name}: {p.age} лет")
    
    print("\n--- 3.5 Сортировка по имени ---")
    sorted_by_name = col.sort_by_name()
    for p in sorted_by_name:
        print(f"     - {p.name}")
    
    print("\n--- 3.6 Удаление по индексу ---")
    print(f"   До: {len(col)} пациентов")
    col.remove_at(0)
    print(f"   После: {len(col)} пациентов")


def scenario_4():
    """Сценарий 4: Фильтрация и полиморфизм."""
    print("\n" + "="*60)
    print("СЦЕНАРИЙ 4: ФИЛЬТРАЦИЯ И ПОЛИМОРФИЗМ")
    print("="*60)
    
    col = PatientCollection()
    patients = create_test_data()
    
    for p in patients:
        col.add(p)
    
    print("\n--- 4.1 Пожилые пациенты (is_senior) ---")
    for p in col:
        if p.is_senior():
            print(f"     - {p.name}: {p.age} лет")
    
    print("\n--- 4.2 Срочная помощь (needs_urgent_care) ---")
    for p in col:
        if p.needs_urgent_care():
            print(f"     - {p.name}: {p.diagnosis} [СРОЧНО!]")
    
    print("\n--- 4.3 Фильтрация по типу (isinstance) ---")
    inpatients = [p for p in col if isinstance(p, Inpatient)]
    outpatients = [p for p in col if isinstance(p, Outpatient)]
    print(f"   Стационарных: {len(inpatients)}")
    print(f"   Амбулаторных: {len(outpatients)}")
    print(f"   Обычных: {len(col) - len(inpatients) - len(outpatients)}")
    
    print("\n--- 4.4 Полиморфизм get_cost() ---")
    for p in col:
        print(f"   {p.name} ({p.get_type()}): {p.get_cost()} руб.")
    
    print("\n--- 4.5 Полиморфизм get_info() ---")
    for p in col:
        print(f"   {p.get_info()}")


def scenario_5():
    """Сценарий 5: Бизнес-сценарии."""
    print("\n" + "="*60)
    print("СЦЕНАРИЙ 5: БИЗНЕС-СЦЕНАРИИ")
    print("="*60)
    
    col = PatientCollection()
    patients = create_test_data()
    
    for p in patients:
        col.add(p)
    
    print("\n--- 5.1 Общая стоимость лечения ---")
    total = sum(p.get_cost() for p in col)
    print(f"   Итого: {total} руб.")
    
    print("\n--- 5.2 Детализация по типам ---")
    inpatient_cost = sum(p.get_cost() for p in col if isinstance(p, Inpatient))
    outpatient_cost = sum(p.get_cost() for p in col if isinstance(p, Outpatient))
    print(f"   Стационарные: {inpatient_cost} руб.")
    print(f"   Амбулаторные: {outpatient_cost} руб.")
    
    print("\n--- 5.3 Возрастная структура ---")
    seniors = [p for p in col if p.age >= 65]
    adults = [p for p in col if 18 <= p.age < 65]
    children = [p for p in col if p.age < 18]
    print(f"   Дети (0-17): {len(children)}")
    print(f"   Взрослые (18-64): {len(adults)}")
    print(f"   Пожилые (65+): {len(seniors)}")
    
    print("\n--- 5.4 Нагрузка на врачей ---")
    doctors = {}
    for p in col:
        doc = p.doctor
        doctors[doc] = doctors.get(doc, 0) + 1
    for doc, count in doctors.items():
        print(f"   {doc}: {count}")
    
    print("\n--- 5.5 Стационарные пациенты ---")
    for p in col:
        if isinstance(p, Inpatient):
            print(f"   {p.name}: палата {p.ward}, дней: {p.get_days()}")
    
    print("\n--- 5.6 Амбулаторные пациенты ---")
    for p in col:
        if isinstance(p, Outpatient):
            print(f"   {p.name}: {p.visits} визитов")
            p.add_visit()
    
    print("\n--- 5.7 После дополнительных визитов ---")
    for p in col:
        if isinstance(p, Outpatient):
            print(f"   {p.name}: теперь {p.visits} визитов, стоимость: {p.get_cost()} руб.")
    
    print("\n--- 5.8 Экстренная госпитализация ---")
    for p in col:
        if p.needs_urgent_care():
            print(f"   {p.name} -> {p.diagnosis.upper()}! Срочно!")
    
    print("\n--- 5.9 Итоговая статистика ---")
    print(f"   Всего: {len(col)} пациентов")
    print(f"   Общая стоимость: {sum(p.get_cost() for p in col)} руб.")
    avg_age = sum(p.age for p in col) / len(col)
    print(f"   Средний возраст: {avg_age:.1f} лет")


def extra_demo():
    """Дополнительная демонстрация дочерних методов."""
    print("\n" + "="*60)
    print("ДОПОЛНИТЕЛЬНО: МЕТОДЫ ДОЧЕРНИХ КЛАССОВ")
    print("="*60)
    
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    tomorrow = today + timedelta(days=1)
    
    print("\n--- Inpatient методы ---")
    inp = Inpatient("T01", "Тест Стационарный", 50, "Тест", "Врач", "101", yesterday)
    print(f"   Создан: {inp}")
    print(f"   Дней в больнице: {inp.get_days()}")
    inp.discharge()
    
    print("\n--- Outpatient методы ---")
    outp = Outpatient("T02", "Тест Амбулаторный", 30, "Тест", "Врач", tomorrow)
    print(f"   Создан: {outp}")
    print(f"   Стоимость: {outp.get_cost()} руб.")
    outp.add_visit()
    print(f"   После визита: {outp}")
    print(f"   Стоимость: {outp.get_cost()} руб.")


def main():
    print("\n" + "█"*60)
    print("ЛАБОРАТОРНАЯ РАБОТА №3 - НАСЛЕДОВАНИЕ")
    print("Предметная область: МЕДИЦИНА")
    print("Оценка: 5")
    print("█"*60)
    
    scenario_1()
    scenario_2()
    scenario_3()
    scenario_4()
    scenario_5()
    extra_demo()
    
    print("\n" + "█"*60)
    print("ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА")
    print("█"*60 + "\n")


if __name__ == "__main__":
    main()