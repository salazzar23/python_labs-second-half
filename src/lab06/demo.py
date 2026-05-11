"""
Лабораторная работа №6 - Generics и typing
Демонстрация с 3 сценариями
Предметная область: Медицина
"""

from datetime import datetime, timedelta
from models import Patient, Inpatient, Outpatient
from container import (
    TypedCollection, TypedDisplayCollection, TypedScoreCollection,
    Displayable, Scorable
)


def create_test_patients():
    """Создание тестовых пациентов."""
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    tomorrow = today + timedelta(days=1)
    
    return [
        Patient("P001", "Иванов Иван", 45, "Гипертония", "Кардиолог"),
        Patient("P002", "Новиков Павел", 32, "Здоров", "Терапевт"),
        Inpatient("P003", "Петрова Мария", 68, "Инфаркт", "Кардиолог", "301", yesterday),
        Inpatient("P004", "Сидоров Алексей", 72, "Инсульт", "Невролог", "405", yesterday),
        Outpatient("P005", "Кузнецова Елена", 35, "Гастрит", "Гастроэнтеролог", tomorrow),
        Outpatient("P006", "Смирнов Дмитрий", 58, "Диабет", "Эндокринолог", tomorrow),
    ]


def print_separator(title: str) -> None:
    """Печать разделителя."""
    print("\n" + "="*70)
    print(f" {title}")
    print("="*70)


# ============================================================================
# СЦЕНАРИЙ 1: Generics и типизация (оценка 3)
# ============================================================================

def scenario_1_generics() -> None:
    """Сценарий 1: Generic-коллекция и аннотации типов."""
    print_separator("СЦЕНАРИЙ 1: GENERIC-КОЛЛЕКЦИЯ TYPEDCOLLECTION")
    
    # Создаём типизированную коллекцию для Patient
    collection: TypedCollection[Patient] = TypedCollection()
    patients = create_test_patients()
    
    print("\n--- 1.1 Добавление пациентов в TypedCollection ---")
    for p in patients[:4]:
        collection.add(p)
    
    print("\n--- 1.2 Вывод всех пациентов ---")
    collection.print_all("TypedCollection[Patient]")
    
    print("\n--- 1.3 Доступ по индексу ---")
    print(f"      Первый пациент: {collection[0].name}")
    print(f"      Последний пациент: {collection[-1].name}")
    print(f"      Всего пациентов: {len(collection)}")
    
    print("\n--- 1.4 Перебор через for ---")
    for i, p in enumerate(collection):
        print(f"      {i+1}. {p.name} - {p.get_short_info()}")
    
    print("\n--- 1.5 Удаление пациента ---")
    collection.remove(patients[1])


# ============================================================================
# СЦЕНАРИЙ 2: find, filter, map (оценка 4)
# ============================================================================

def scenario_2_find_filter_map() -> None:
    """Сценарий 2: Методы find, filter, map с аннотациями."""
    print_separator("СЦЕНАРИЙ 2: FIND, FILTER, MAP")
    
    collection: TypedCollection[Patient] = TypedCollection()
    patients = create_test_patients()
    
    for p in patients:
        collection.add(p)
    
    print(f"\n--- 2.1 find() - поиск элемента ---")
    print("   Поиск пациента с именем 'Петрова':")
    found = collection.find(lambda p: "Петрова" in p.name)
    print(f"   Результат: {found.name if found else 'Не найден'}")
    
    print("\n   Поиск пациента с диагнозом 'Рак' (не существует):")
    not_found = collection.find(lambda p: "рак" in p.diagnosis.lower())
    print(f"   Результат: {'Найден' if not_found else 'Не найден'}")
    
    print("\n--- 2.2 filter() - фильтрация элементов ---")
    print("   Фильтр: пациенты старше 60 лет:")
    seniors = collection.filter(lambda p: p.age > 60)
    for p in seniors:
        print(f"      - {p.name} ({p.age} лет)")
    
    print("\n   Фильтр: стационарные пациенты (Inpatient):")
    inpatients = collection.filter(lambda p: isinstance(p, Inpatient))
    for p in inpatients:
        print(f"      - {p.name} - {p.get_type()}")
    
    print("\n--- 2.3 map() - преобразование элементов (меняет тип!) ---")
    print("   map: получить список имён пациентов (Patient -> str):")
    names: list[str] = collection.map(lambda p: p.name)
    for i, name in enumerate(names):
        print(f"      {i+1}. {name}")
    
    print("\n   map: получить список стоимостей лечения (Patient -> float):")
    costs: list[float] = collection.map(lambda p: p.get_cost())
    print(f"      Стоимости: {costs}")
    print(f"      Общая стоимость: {sum(costs)} руб.")
    
    print("\n   map: получить строковое представление (Patient -> str):")
    infos = collection.map(lambda p: p.get_short_info())
    for i, info in enumerate(infos):
        print(f"      {i+1}. {info}")
    
    print("\n--- 2.4 Демонстрация смены типа через map ---")
    print("   Было: TypedCollection[Patient]")
    print("   Стало: list[str] после map с lambda p: p.name")
    print("   Стало: list[float] после map с lambda p: p.get_cost()")
    print("   Это показывает зачем нужен второй TypeVar (R)")


# ============================================================================
# СЦЕНАРИЙ 3: Protocol и структурная типизация (оценка 5)
# ============================================================================

def scenario_3_protocols() -> None:
    """Сценарий 3: Protocol и структурная типизация."""
    print_separator("СЦЕНАРИЙ 3: PROTOCOL И СТРУКТУРНАЯ ТИПИЗАЦИЯ")
    
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    tomorrow = today + timedelta(days=1)
    
    # Создаём объекты разных классов из иерархии
    # Ни один из них не наследуется от Displayable или Scorable!
    # Но у всех есть методы display() и get_score()
    
    patient = Patient("P001", "Иванов Иван", 45, "Гипертония", "Кардиолог")
    inpatient = Inpatient("P002", "Петрова Мария", 68, "Инфаркт", "Кардиолог", "301", yesterday)
    outpatient = Outpatient("P003", "Кузнецова Елена", 35, "Гастрит", "Гастроэнтеролог", tomorrow)
    
    print("\n--- 3.1 TypedDisplayCollection[D] с bound=Displayable ---")
    print("   Классы не наследуются от Displayable, но имеют метод display()")
    print("   → Они структурно совместимы с протоколом!")
    
    display_collection: TypedDisplayCollection[Displayable] = TypedDisplayCollection()
    
    print("\n   Добавление объектов в Displayable коллекцию:")
    display_collection.add(patient)      # Patient имеет display()
    display_collection.add(inpatient)    # Inpatient имеет display()
    display_collection.add(outpatient)   # Outpatient имеет display()
    
    print("\n   Вывод через display() метод:")
    display_collection.display_all()
    
    print("\n--- 3.2 TypedScoreCollection[S] с bound=Scorable ---")
    print("   Классы имеют метод get_score() → подходят под протокол Scorable")
    
    score_collection: TypedScoreCollection[Scorable] = TypedScoreCollection()
    
    score_collection.add(patient)
    score_collection.add(inpatient)
    score_collection.add(outpatient)
    
    print("\n   Вывод с оценками (score):")
    score_collection.print_scores()
    
    print("\n--- 3.3 Сортировка по score() ---")
    sorted_by_score = score_collection.get_sorted_by_score()
    print("   Пациенты, отсортированные по приоритету (от highest к lowest):")
    for i, p in enumerate(sorted_by_score):
        score = p.get_score()
        print(f"      {i+1}. {p.display()} | Score: {score}")
    
    print("\n--- 3.4 Демонстрация структурной типизации ---")
    print("   Ключевой момент: классы Patient, Inpatient, Outpatient")
    print("   НЕ наследуются от Displayable и Scorable явно.")
    print("   Но они имеют нужные методы (display, get_score).")
    print("   Python принимает их благодаря структурной типизации (Protocol).")
    print("   Это и есть 'утиная типизация' на уровне типов!")


# ============================================================================
# MAIN
# ============================================================================

def main() -> None:
    print("\n" + "█"*70)
    print("ЛАБОРАТОРНАЯ РАБОТА №6 - GENERICS И TYPING")
    print("Предметная область: МЕДИЦИНА")
    print("█"*70)
    
    scenario_1_generics()
    scenario_2_find_filter_map()
    scenario_3_protocols()
    
    print("\n" + "█"*70)
    print("ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА")
    print("█"*70 + "\n")


if __name__ == "__main__":
    main()