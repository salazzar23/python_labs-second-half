"""
Лабораторная работа №5 - Функции как аргументы. Стратегии и делегаты.
Демонстрация с 3 сценариями
Предметная область: Медицина
"""

from datetime import datetime, timedelta
from models import Patient, Inpatient, Outpatient
from collection import PatientCollection
from strategies import (
    by_name, by_age, by_cost, by_type_then_name,
    is_senior, is_urgent, is_expensive, is_inpatient,
    make_age_filter, make_cost_filter, make_sort_by_field,
    DiscountStrategy, SortStrategy, ReportStrategy
)


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


def print_separator(title: str):
    """Печать разделителя."""
    print("\n" + "="*70)
    print(f" {title}")
    print("="*70)


# ============================================================================
# СЦЕНАРИЙ 1: Функции-стратегии для сортировки и фильтры (оценка 3)
# ============================================================================

def scenario_1_sorting_and_filtering():
    """Сценарий 1: Сортировка тремя разными стратегиями и фильтрация."""
    print_separator("СЦЕНАРИЙ 1: СОРТИРОВКА И ФИЛЬТРАЦИЯ (оценка 3)")
    
    collection = PatientCollection()
    patients = create_test_data()
    
    for p in patients:
        collection.add(p)
    
    # 1.1 Исходная коллекция
    print("\n--- 1.1 Исходная коллекция ---")
    collection.print_all("Исходная коллекция")
    
    # 1.2 Сортировка по имени
    print("\n--- 1.2 Сортировка по имени (by_name) ---")
    sorted_by_name = collection.sort_by(by_name)
    sorted_by_name.print_all("Сортировка по имени")
    
    # 1.3 Сортировка по возрасту
    print("\n--- 1.3 Сортировка по возрасту (by_age) ---")
    sorted_by_age = collection.sort_by(by_age)
    sorted_by_age.print_all("Сортировка по возрасту")
    
    # 1.4 Сортировка по стоимости лечения
    print("\n--- 1.4 Сортировка по стоимости лечения (by_cost) ---")
    sorted_by_cost = collection.sort_by(by_cost, reverse=True)
    sorted_by_cost.print_all("Сортировка по стоимости (дорогие сначала)")
    
    # 1.5 Фильтрация: пожилые пациенты
    print("\n--- 1.5 Фильтрация: пожилые пациенты (is_senior) ---")
    seniors = collection.filter_by(is_senior)
    seniors.print_all("Пожилые пациенты")
    
    # 1.6 Фильтрация: срочная помощь
    print("\n--- 1.6 Фильтрация: срочная помощь (is_urgent) ---")
    urgent = collection.filter_by(is_urgent)
    urgent.print_all("Требуют срочной помощи")
    
    # 1.7 Фильтрация через lambda
    print("\n--- 1.7 Фильтрация через lambda (возраст > 60) ---")
    age_filter = collection.filter_by(lambda p: p.age > 60)
    age_filter.print_all("Пациенты старше 60 лет")
    
    # 1.8 Сортировка через lambda
    print("\n--- 1.8 Сортировка через lambda (по длине имени) ---")
    sorted_by_name_len = collection.sort_by(lambda p: len(p.name))
    sorted_by_name_len.print_all("Сортировка по длине имени")


# ============================================================================
# СЦЕНАРИЙ 2: Map, фабрики функций и методы коллекции (оценка 4)
# ============================================================================

def scenario_2_map_and_factories():
    """Сценарий 2: Применение map, фабрик функций, методов sort_by/filter_by."""
    print_separator("СЦЕНАРИЙ 2: MAP, ФАБРИКИ И МЕТОДЫ КОЛЛЕКЦИИ (оценка 4)")
    
    collection = PatientCollection()
    patients = create_test_data()
    
    for p in patients:
        collection.add(p)
    
    # 2.1 Преобразование через map (имена)
    print("\n--- 2.1 map(): список имён пациентов ---")
    names = collection.map_to(lambda p: p.name)
    for i, name in enumerate(names, 1):
        print(f"      {i}. {name}")
    
    # 2.2 Преобразование через map (краткая информация)
    print("\n--- 2.2 map(): краткая информация о пациентах ---")
    info_list = collection.map_to(lambda p: p.get_short_info())
    for i, info in enumerate(info_list, 1):
        print(f"      {i}. {info}")
    
    # 2.3 map: извлечение стоимости лечения
    print("\n--- 2.3 map(): стоимость лечения всех пациентов ---")
    costs = collection.map_to(lambda p: p.get_cost())
    print(f"      Стоимости: {costs}")
    print(f"      Общая стоимость: {sum(costs)} руб.")
    
    # 2.4 Фабрика: фильтр по возрастному диапазону
    print("\n--- 2.4 Фабрика: фильтр по возрасту (30-50 лет) ---")
    age_filter = make_age_filter(30, 50)
    filtered = collection.filter_by(age_filter)
    filtered.print_all("Пациенты 30-50 лет")
    
    # 2.5 Фабрика: фильтр по стоимости
    print("\n--- 2.5 Фабрика: фильтр по стоимости (<= 5000 руб.) ---")
    cost_filter = make_cost_filter(5000)
    cheap_patients = collection.filter_by(cost_filter)
    cheap_patients.print_all("Лечение стоит до 5000 руб.")
    
    # 2.6 Фабрика: создание ключа сортировки
    print("\n--- 2.6 Фабрика: сортировка по полю diagnosis ---")
    sort_by_diagnosis = make_sort_by_field("diagnosis")
    sorted_by_diag = collection.sort_by(sort_by_diagnosis)
    sorted_by_diag.print_all("Сортировка по диагнозу")
    
    # 2.7 Методы коллекции sort_by и filter_by
    print("\n--- 2.7 Метод sort_by() коллекции ---")
    collection.sort_by(by_age).print_all("Сортировка через метод коллекции")
    
    print("\n--- 2.8 Метод filter_by() коллекции ---")
    collection.filter_by(is_inpatient).print_all("Только стационарные")
    
    # 2.9 Сравнение lambda и именованной функции
    print("\n--- 2.9 Сравнение: lambda vs именованная функция ---")
    print("      Через lambda: collection.filter_by(lambda p: p.age > 65)")
    print("      Через функцию: collection.filter_by(is_senior)")
    print("      Результат одинаковый:")

    seniors_lambda = collection.filter_by(lambda p: p.age > 65)
    seniors_func = collection.filter_by(is_senior)
    print(f"      lambda дал {len(seniors_lambda)} пациентов")
    print(f"      is_senior дал {len(seniors_func)} пациентов")


# ============================================================================
# СЦЕНАРИЙ 3: Паттерн Стратегия и цепочки операций (оценка 5)
# ============================================================================

def scenario_3_strategy_and_chains():
    """Сценарий 3: Паттерн Стратегия, callable-объекты, цепочки операций."""
    print_separator("СЦЕНАРИЙ 3: ПАТТЕРН СТРАТЕГИЯ И ЦЕПОЧКИ (оценка 5)")
    
    collection = PatientCollection()
    patients = create_test_data()
    
    for p in patients:
        collection.add(p)
    
    # 3.1 Callable-объект DiscountStrategy
    print("\n--- 3.1 Callable-объект DiscountStrategy ---")
    discount_10 = DiscountStrategy(10)
    discount_20 = DiscountStrategy(20)
    
    print(f"      Стратегия: {discount_10}")
    for p in collection.get_all()[:3]:
        original = p.get_cost()
        discounted = discount_10(p)
        print(f"      {p.name}: {original} руб. -> {discounted} руб. (скидка 10%)")
    
    # 3.2 Callable-объект SortStrategy
    print("\n--- 3.2 Callable-объект SortStrategy ---")
    sort_by_name_strategy = SortStrategy(by_name, name="Сортировка по имени")
    sort_by_age_strategy = SortStrategy(by_age, name="Сортировка по возрасту")
    
    print(f"      Стратегия: {sort_by_name_strategy}")
    sorted_by_name_obj = sort_by_name_strategy(collection.get_all())
    for p in sorted_by_name_obj[:3]:
        print(f"        - {p.name}")
    
    # 3.3 Callable-объект ReportStrategy
    print("\n--- 3.3 Callable-объект ReportStrategy ---")
    simple_report = ReportStrategy("simple")
    detailed_report = ReportStrategy("detailed")
    
    print(f"      {simple_report}")
    print(simple_report(collection.get_all()))
    
    # 3.4 Цепочка операций filter → sort
    print("\n--- 3.4 Цепочка: filter_by → sort_by ---")
    result = (collection
              .filter_by(is_inpatient)
              .sort_by(by_age))
    result.print_all("Стационарные, отсортированные по возрасту")
    
    # 3.5 Цепочка filter → sort → apply
    print("\n--- 3.5 Цепочка: filter_by → sort_by → apply ---")
    
    # Создаём функцию для применения скидки
    def apply_discount_to_patient(patient):
        if patient.get_cost() > 0:
            print(f"        Скидка для {patient.name}: {patient.get_cost()} -> {patient.get_cost() * 0.9} руб.")
    
    (collection
     .filter_by(is_expensive)
     .sort_by(by_cost, reverse=True)
     .apply(apply_discount_to_patient))
    
    # 3.6 Метод chain() - одна цепочка
    print("\n--- 3.6 Метод chain() ---")
    result2 = collection.chain(
        filter_pred=is_urgent,
        sort_key=by_cost,
        sort_reverse=True
    )
    result2.print_all("Срочные пациенты, отсортированные по стоимости")
    
    # 3.7 Замена стратегии без изменения кода коллекции
    print("\n--- 3.7 Замена стратегии без изменения кода коллекции ---")
    
    strategies = [by_name, by_age, by_cost]
    strategy_names = ["по имени", "по возрасту", "по стоимости"]
    
    for strategy, name in zip(strategies, strategy_names):
        sorted_col = collection.sort_by(strategy)
        first_three = [p.name for p in sorted_col.get_all()[:3]]
        print(f"      Сортировка {name}: {first_three}")
    
    # 3.8 Полная цепочка с демонстрацией результата
    print("\n--- 3.8 Полная цепочка: фильтр → сортировка → применение ---")
    
    # Создаём отчёт через стратегию
    report_strategy = ReportStrategy("detailed")
    
    final_result = (collection
                    .filter_by(is_senior)
                    .sort_by(by_age, reverse=True))
    
    print("\n      ИТОГОВЫЙ ОТЧЁТ ПО ПОЖИЛЫМ ПАЦИЕНТАМ:")
    print(report_strategy(final_result.get_all()))


# ============================================================================
# MAIN
# ============================================================================

def main():
    print("\n" + "█"*70)
    print("ЛАБОРАТОРНАЯ РАБОТА №5 - ФУНКЦИИ КАК АРГУМЕНТЫ. СТРАТЕГИИ И ДЕЛЕГАТЫ.")
    print("Предметная область: МЕДИЦИНА")
    print("█"*70)
    
    scenario_1_sorting_and_filtering()
    scenario_2_map_and_factories()
    scenario_3_strategy_and_chains()
    
    print("\n" + "█"*70)
    print("ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА")
    print("█"*70 + "\n")


if __name__ == "__main__":
    main()