"""
Лабораторная работа №6 - Generics и typing
Демонстрация с одним универсальным Generic-классом TypedCollection[T]
"""

from datetime import datetime, timedelta
from models import Patient, Inpatient, Outpatient
from container import TypedCollection, Displayable, Scorable, D, S


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


def print_separator(title: str):
    print("\n" + "="*70)
    print(f" {title}")
    print("="*70)


# ============================================================================
# СЦЕНАРИЙ 1: Generic-коллекция с Patient (оценка 3)
# ============================================================================

def scenario_1_generics():
    print_separator("СЦЕНАРИЙ 1: TYPEDCOLLECTION С PATIENT")
    
    col: TypedCollection[Patient] = TypedCollection()
    patients = create_test_patients()
    
    print("\n--- 1.1 Добавление пациентов ---")
    for p in patients[:4]:
        col.add(p)
    
    print("\n--- 1.2 Вывод всех пациентов ---")
    col.print_all("TypedCollection[Patient]")
    
    print("\n--- 1.3 Доступ по индексу ---")
    print(f"      Первый: {col[0].name}")
    print(f"      Последний: {col[-1].name}")
    print(f"      Всего: {len(col)}")
    
    print("\n--- 1.4 Итерация через for ---")
    for i, p in enumerate(col):
        print(f"      {i+1}. {p.name}")
    
    print("\n--- 1.5 Удаление ---")
    col.remove(patients[1])


# ============================================================================
# СЦЕНАРИЙ 2: find, filter, map (оценка 4)
# ============================================================================

def scenario_2_find_filter_map():
    print_separator("СЦЕНАРИЙ 2: FIND, FILTER, MAP")
    
    col: TypedCollection[Patient] = TypedCollection()
    patients = create_test_patients()
    
    for p in patients:
        col.add(p)
    
    print("\n--- 2.1 find() ---")
    print("   Поиск 'Петрова':")
    found = col.find(lambda p: "Петрова" in p.name)
    print(f"   Результат: {found.name if found else 'Не найден'}")
    
    print("\n   Поиск 'Рак' (не существует):")
    not_found = col.find(lambda p: "рак" in p.diagnosis.lower())
    print(f"   Результат: {'Найден' if not_found else 'Не найден'}")
    
    print("\n--- 2.2 filter() ---")
    seniors = col.filter(lambda p: p.age > 60)
    print("   Пациенты старше 60 лет:")
    for p in seniors:
        print(f"      - {p.name} ({p.age} лет)")
    
    print("\n--- 2.3 map() ---")
    names = col.map(lambda p: p.name)
    print(f"   Имена: {names}")
    
    costs = col.map(lambda p: p.get_cost())
    print(f"   Стоимости: {costs}")
    print(f"   Общая стоимость: {sum(costs)} руб.")
    
    print("\n--- 2.4 Смена типа через map ---")
    print("   Было: TypedCollection[Patient]")
    print("   Стало: list[str] после map(lambda p: p.name)")
    print("   Стало: list[float] после map(lambda p: p.get_cost())")


# ============================================================================
# СЦЕНАРИЙ 3: Protocol и структурная типизация (оценка 5)
# ============================================================================

def scenario_3_protocols():
    print_separator("СЦЕНАРИЙ 3: PROTOCOL И СТРУКТУРНАЯ ТИПИЗАЦИЯ")
    
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    tomorrow = today + timedelta(days=1)
    
    patient = Patient("P001", "Иванов Иван", 45, "Гипертония", "Кардиолог")
    inpatient = Inpatient("P002", "Петрова Мария", 68, "Инфаркт", "Кардиолог", "301", yesterday)
    outpatient = Outpatient("P003", "Кузнецова Елена", 35, "Гастрит", "Гастроэнтеролог", tomorrow)
    
    print("\n--- 3.1 TypedCollection с ограничением Displayable ---")
    display_col: TypedCollection[D] = TypedCollection()
    display_col.add(patient)
    display_col.add(inpatient)
    display_col.add(outpatient)
    display_col.display_all()
    
    print("\n--- 3.2 TypedCollection с ограничением Scorable ---")
    score_col: TypedCollection[S] = TypedCollection()
    score_col.add(patient)
    score_col.add(inpatient)
    score_col.add(outpatient)
    score_col.print_scores()
    
    print("\n--- 3.3 Сортировка по score() ---")
    sorted_patients = score_col.get_sorted_by_score()
    print("   Пациенты по приоритету (от highest к lowest):")
    for i, p in enumerate(sorted_patients):
        score = p.get_score() if hasattr(p, 'get_score') else 0
        print(f"      {i+1}. {p.name} | Score: {score}")
    
    print("\n--- 3.4 Структурная совместимость ---")
    print("   Классы НЕ наследуются от Displayable/Scorable.")
    print("   Но они имеют методы display() и get_score().")
    print("   Python принимает их благодаря Protocol.")


# ============================================================================
# MAIN
# ============================================================================

def main():
    print("\n" + "█"*70)
    print("ЛАБОРАТОРНАЯ РАБОТА №6 - GENERICS И TYPING")
    print("Один универсальный Generic-класс TypedCollection[T]")
    print("█"*70)
    
    scenario_1_generics()
    scenario_2_find_filter_map()
    scenario_3_protocols()
    
    print("\n" + "█"*70)
    print("ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА")
    print("█"*70 + "\n")


if __name__ == "__main__":
    main()