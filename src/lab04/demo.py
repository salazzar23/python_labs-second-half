"""
Лабораторная работа №4 - Интерфейсы и абстрактные классы (ABC)
Демонстрация работы интерфейсов Printable и Comparable
Предметная область: Медицина
"""

from datetime import datetime, timedelta
import functools
from interfaces import Printable, Comparable
from models import Patient, Inpatient, Outpatient
from collection import PatientCollection


# ============================================================================
# УНИВЕРСАЛЬНЫЕ ФУНКЦИИ (РАБОТА ЧЕРЕЗ ИНТЕРФЕЙС)
# ============================================================================

def print_all(items: list[Printable]) -> None:
    """
    Универсальная функция вывода.
    Работает с любыми объектами, реализующими интерфейс Printable.
    """
    for item in items:
        print(f"  {item.get_short_info()}")


def compare_objects(a: Comparable, b: Comparable) -> int:
    """
    Функция сравнения для использования с cmp_to_key.
    """
    if hasattr(a, 'compare'):
        return a.compare(b)
    raise TypeError("Объект не поддерживает сравнение")


def get_sorted(items: list) -> list:
    """
    Универсальная функция сортировки.
    Работает с любыми объектами, реализующими интерфейс Comparable.
    Использует cmp_to_key для корректной сортировки через метод compare().
    """
    def cmp_func(x, y):
        if hasattr(x, 'compare'):
            return x.compare(y)
        if x < y:
            return -1
        elif x > y:
            return 1
        return 0
    
    return sorted(items, key=functools.cmp_to_key(cmp_func))


def create_test_data():
    """Создание тестовых объектов."""
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    two_days_ago = today - timedelta(days=2)
    tomorrow = today + timedelta(days=1)
    next_week = today + timedelta(days=7)
    
    return [
        Patient("P001", "Иванов Иван", 45, "Гипертония", "Кардиолог"),
        Patient("P008", "Новиков Павел", 32, "Здоров", "Терапевт"),
        Inpatient("P002", "Петрова Мария", 68, "Инфаркт", "Кардиолог", "301", yesterday),
        Inpatient("P003", "Сидоров Алексей", 72, "Инсульт", "Невролог", "405", yesterday),
        Inpatient("P006", "Васильева Анна", 25, "Аппендицит", "Хирург", "210", yesterday),
        Outpatient("P004", "Кузнецова Елена", 35, "Гастрит", "Гастроэнтеролог", tomorrow),
        Outpatient("P005", "Смирнов Дмитрий", 58, "Диабет", "Эндокринолог", next_week),
        Outpatient("P007", "Михайлов Сергей", 80, "Аритмия", "Кардиолог", next_week),
    ]


# ============================================================================
# СЦЕНАРИЙ 1: Реализация интерфейсов в классах
# ============================================================================

def scenario_1_interface_implementation():
    """Сценарий 1: Демонстрация реализации интерфейсов в разных классах."""
    print("\n" + "="*70)
    print("СЦЕНАРИЙ 1: РЕАЛИЗАЦИЯ ИНТЕРФЕЙСОВ В КЛАССАХ")
    print("="*70)
    
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    tomorrow = today + timedelta(days=1)
    
    p1 = Patient("P001", "Иванов Иван", 45, "Гипертония", "Кардиолог")
    p2 = Inpatient("P002", "Петрова Мария", 68, "Инфаркт", "Кардиолог", "301", yesterday)
    p3 = Outpatient("P003", "Кузнецова Елена", 35, "Гастрит", "Гастроэнтеролог", tomorrow)
    
    print("\n--- Объекты разных типов ---")
    print(f"Обычный: {p1}")
    print(f"Стационарный: {p2}")
    print(f"Амбулаторный: {p3}")
    
    print("\n--- Метод get_short_info() (Printable) ---")
    print(f"  {p1.get_short_info()}")
    print(f"  {p2.get_short_info()}")
    print(f"  {p3.get_short_info()}")
    
    print("\n--- Метод compare() (Comparable) ---")
    print(f"  {p1.name} ({p1.age}) vs {p2.name} ({p2.age}) -> {p1.compare(p2)}")
    print(f"  {p2.name} ({p2.age}) vs {p1.name} ({p1.age}) -> {p2.compare(p1)}")
    print(f"  {p1.name} ({p1.age}) vs {p1.name} ({p1.age}) -> {p1.compare(p1)}")
    
    print("\n--- Разные критерии сравнения в дочерних классах ---")
    p4 = Inpatient("P004", "Сидоров Алексей", 72, "Инсульт", "Невролог", "405", yesterday)
    p5 = Outpatient("P005", "Смирнов Дмитрий", 58, "Диабет", "Эндокринолог", tomorrow)
    p5.add_visit()
    p5.add_visit()
    
    print(f"  Inpatient {p2.name} (дней: {p2.get_days()}) vs {p4.name} (дней: {p4.get_days()}) -> {p2.compare(p4)}")
    print(f"  Outpatient {p3.name} (визитов: {p3.visits}) vs {p5.name} (визитов: {p5.visits}) -> {p3.compare(p5)}")


# ============================================================================
# СЦЕНАРИЙ 2: Универсальные функции через интерфейс
# ============================================================================

def scenario_2_universal_functions():
    """Сценарий 2: Работа универсальных функций через интерфейсы."""
    print("\n" + "="*70)
    print("СЦЕНАРИЙ 2: УНИВЕРСАЛЬНЫЕ ФУНКЦИИ ЧЕРЕЗ ИНТЕРФЕЙС")
    print("="*70)
    
    patients = create_test_data()
    
    print("\n--- Функция print_all() работает с любыми Printable ---")
    print_all(patients)
    
    print("\n--- Функция get_sorted() сортирует Comparable объекты ---")
    sorted_by_age = get_sorted(patients)
    print("Отсортировано по возрасту:")
    for p in sorted_by_age:
        print(f"  {p.name}: {p.age} лет")
    
    print("\n--- Фильтрация и сортировка только Inpatient ---")
    inpatients = [p for p in patients if isinstance(p, Inpatient)]
    sorted_inpatients = get_sorted(inpatients)
    print("Стационарные пациенты (сравнение по дням):")
    for p in sorted_inpatients:
        print(f"  {p.name}: {p.get_days()} дней")
    
    print("\n--- Фильтрация и сортировка только Outpatient ---")
    outpatients = [p for p in patients if isinstance(p, Outpatient)]
    sorted_outpatients = get_sorted(outpatients)
    print("Амбулаторные пациенты (сравнение по визитам):")
    for p in sorted_outpatients:
        print(f"  {p.name}: {p.visits} визитов")


# ============================================================================
# СЦЕНАРИЙ 3: Проверка типов и множественная реализация
# ============================================================================

def scenario_3_isinstance_and_multiple():
    """Сценарий 3: Проверка isinstance и множественная реализация интерфейсов."""
    print("\n" + "="*70)
    print("СЦЕНАРИЙ 3: ПРОВЕРКА ТИПОВ И МНОЖЕСТВЕННАЯ РЕАЛИЗАЦИЯ")
    print("="*70)
    
    patients = create_test_data()
    
    print("\n--- Проверка реализации интерфейсов (isinstance) ---")
    for p in patients[:5]:
        is_printable = isinstance(p, Printable)
        is_comparable = isinstance(p, Comparable)
        print(f"  {p.name}: Printable={is_printable}, Comparable={is_comparable}")
    
    print("\n--- Фильтрация коллекции по интерфейсу Printable ---")
    printable_objects = [p for p in patients if isinstance(p, Printable)]
    print(f"  Объектов, реализующих Printable: {len(printable_objects)}")
    
    print("\n--- Фильтрация коллекции по интерфейсу Comparable ---")
    comparable_objects = [p for p in patients if isinstance(p, Comparable)]
    print(f"  Объектов, реализующих Comparable: {len(comparable_objects)}")
    
    print("\n--- Демонстрация полиморфизма через интерфейс (без if type ==) ---")
    print("  Вызов get_short_info() у разных объектов:")
    for p in patients[:5]:
        print(f"    {p.get_short_info()}")


# ============================================================================
# СЦЕНАРИЙ 4: Интеграция с коллекцией из ЛР-2
# ============================================================================

def scenario_4_collection_integration():
    """Сценарий 4: Интеграция интерфейсов с коллекцией PatientCollection."""
    print("\n" + "="*70)
    print("СЦЕНАРИЙ 4: ИНТЕГРАЦИЯ С КОЛЛЕКЦИЕЙ PATIENTCOLLECTION")
    print("="*70)
    
    collection = PatientCollection()
    patients = create_test_data()
    
    for p in patients:
        collection.add(p)
    
    print(f"\n--- Всего пациентов: {len(collection)} ---")
    
    print("\n--- Фильтрация по интерфейсу Printable (метод get_printable()) ---")
    printable_list = collection.get_printable()
    print(f"  Printable объектов: {len(printable_list)}")
    
    print("\n--- Фильтрация по интерфейсу Comparable (метод get_comparable()) ---")
    comparable_list = collection.get_comparable()
    print(f"  Comparable объектов: {len(comparable_list)}")
    
    print("\n--- Вывод через универсальную функцию print_all() ---")
    print_all(printable_list[:5])
    
    print("\n--- Сортировка объектов через интерфейс Comparable ---")
    sorted_objects = get_sorted(comparable_list)
    print("  Отсортированные объекты (по возрасту для обычных, по дням для стационарных):")
    for p in sorted_objects[:5]:
        if isinstance(p, Inpatient):
            print(f"    {p.name}: {p.get_days()} дней (стационар)")
        else:
            print(f"    {p.name}: {p.age} лет (обычный)")


# ============================================================================
# СЦЕНАРИЙ 5: Полиморфизм через интерфейс (Good-паттерн)
# ============================================================================

def scenario_5_polymorphism():
    """Сценарий 5: Полиморфизм через интерфейс без условных операторов."""
    print("\n" + "="*70)
    print("СЦЕНАРИЙ 5: ПОЛИМОРФИЗМ ЧЕРЕЗ ИНТЕРФЕЙС (GOOD-ПАТТЕРН)")
    print("="*70)
    
    patients = create_test_data()
    
    print("\n--- Плохо (анти-паттерн): проверка типов через if ---")
    print('  if isinstance(p, Inpatient): ... elif isinstance(p, Outpatient): ...')
    
    print("\n--- Хорошо (good-паттерн): полиморфизм через интерфейс ---")
    print("  p.get_short_info() - один вызов, разное поведение")
    
    print("\n  Результат:")
    for p in patients[:5]:
        print(f"    {p.get_short_info()}")
    
    print("\n--- Единый интерфейс для сортировки ---")
    print("  Один вызов compare() работает по-разному в разных классах:")
    
    p1 = patients[0]  # Patient (обычный, возраст 45)
    p2 = patients[2]  # Inpatient (стационарный, 1 день)
    p3 = patients[6]  # Outpatient (амбулаторный, 1 визит)
    
    print(f"    {p1.name} compare {p2.name}: {p1.compare(p2)} (сравнение по возрасту)")
    print(f"    {p2.name} compare {p1.name}: {p2.compare(p1)} (сравнение по дням в стационаре)")
    
    p4 = Outpatient("P009", "Тестовый", 40, "Тест", "Терапевт", datetime.now() + timedelta(days=1))
    p4.add_visit()
    p4.add_visit()
    print(f"    {p3.name} (визитов: {p3.visits}) compare {p4.name} (визитов: {p4.visits}): {p3.compare(p4)} (сравнение по визитам)")
    
    print("\n--- Преимущества подхода ---")
    print("  1. Код не зависит от конкретных типов")
    print("  2. Легко добавлять новые классы - они просто реализуют интерфейс")
    print("  3. Универсальные функции работают с любыми объектами, реализующими интерфейс")
    print("  4. Нет необходимости менять старый код при добавлении новых классов")


# ============================================================================
# MAIN
# ============================================================================

def main():
    print("\n" + "█"*70)
    print("ЛАБОРАТОРНАЯ РАБОТА №4 - ИНТЕРФЕЙСЫ И АБСТРАКТНЫЕ КЛАССЫ")
    print("Предметная область: МЕДИЦИНА")
    print("█"*70)
    
    scenario_1_interface_implementation()
    scenario_2_universal_functions()
    scenario_3_isinstance_and_multiple()
    scenario_4_collection_integration()
    scenario_5_polymorphism()
    
    print("\n" + "█"*70)
    print("ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА")
    print("█"*70 + "\n")


if __name__ == "__main__":
    main()