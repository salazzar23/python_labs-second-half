"""
Функции-стратегии, фильтры, фабрики и callable-объекты для ЛР-5
Предметная область: Медицина
"""

from typing import Callable, Any
from models import Patient, Inpatient, Outpatient


# ============================================================================
# ФУНКЦИИ-СТРАТЕГИИ ДЛЯ СОРТИРОВКИ
# ============================================================================

def by_name(patient: Patient) -> str:
    """
    Стратегия сортировки по имени пациента.
    
    Args:
        patient: Объект пациента
        
    Returns:
        str: Имя пациента для сортировки
    """
    return patient.name


def by_age(patient: Patient) -> int:
    """
    Стратегия сортировки по возрасту пациента.
    
    Args:
        patient: Объект пациента
        
    Returns:
        int: Возраст пациента для сортировки
    """
    return patient.age


def by_cost(patient: Patient) -> float:
    """
    Стратегия сортировки по стоимости лечения.
    
    Args:
        patient: Объект пациента
        
    Returns:
        float: Стоимость лечения для сортировки
    """
    return patient.get_cost()


def by_type_then_name(patient: Patient) -> tuple:
    """
    Стратегия сортировки: сначала по типу, затем по имени.
    
    Args:
        patient: Объект пациента
        
    Returns:
        tuple: (тип_пациента, имя) для сортировки
    """
    return (patient.get_type(), patient.name)


def by_diagnosis_length(patient: Patient) -> int:
    """
    Стратегия сортировки по длине диагноза.
    
    Args:
        patient: Объект пациента
        
    Returns:
        int: Длина строки диагноза
    """
    return len(patient.diagnosis)


# ============================================================================
# ФУНКЦИИ-ФИЛЬТРЫ
# ============================================================================

def is_senior(patient: Patient) -> bool:
    """
    Фильтр: пожилые пациенты (старше 65 лет).
    
    Args:
        patient: Объект пациента
        
    Returns:
        bool: True если пациент пожилой
    """
    return patient.is_senior()


def is_urgent(patient: Patient) -> bool:
    """
    Фильтр: пациенты, нуждающиеся в срочной помощи.
    
    Args:
        patient: Объект пациента
        
    Returns:
        bool: True если требуется срочная помощь
    """
    return patient.needs_urgent_care()


def is_expensive(patient: Patient) -> bool:
    """
    Фильтр: пациенты с дорогим лечением (стоимость > 5000 руб.).
    
    Args:
        patient: Объект пациента
        
    Returns:
        bool: True если стоимость лечения > 5000
    """
    return patient.get_cost() > 5000


def is_inpatient(patient: Patient) -> bool:
    """
    Фильтр: стационарные пациенты.
    
    Args:
        patient: Объект пациента
        
    Returns:
        bool: True если пациент стационарный
    """
    return isinstance(patient, Inpatient)


def is_outpatient(patient: Patient) -> bool:
    """
    Фильтр: амбулаторные пациенты.
    
    Args:
        patient: Объект пациента
        
    Returns:
        bool: True если пациент амбулаторный
    """
    return isinstance(patient, Outpatient)


# ============================================================================
# ФАБРИКИ ФУНКЦИЙ
# ============================================================================

def make_age_filter(min_age: int, max_age: int) -> Callable[[Patient], bool]:
    """
    Фабрика: создаёт фильтр по возрастному диапазону.
    
    Args:
        min_age: Минимальный возраст
        max_age: Максимальный возраст
        
    Returns:
        Callable: Функция-предикат для фильтрации пациентов по возрасту
    """
    def filter_by_age(patient: Patient) -> bool:
        return min_age <= patient.age <= max_age
    return filter_by_age


def make_cost_filter(max_cost: float) -> Callable[[Patient], bool]:
    """
    Фабрика: создаёт фильтр по максимальной стоимости лечения.
    
    Args:
        max_cost: Максимальная стоимость
        
    Returns:
        Callable: Функция-предикат для фильтрации пациентов по стоимости
    """
    def filter_by_cost(patient: Patient) -> bool:
        return patient.get_cost() <= max_cost
    return filter_by_cost


def make_sort_by_field(field_name: str) -> Callable[[Patient], Any]:
    """
    Фабрика: создаёт функцию-ключ для сортировки по указанному полю.
    
    Args:
        field_name: Имя атрибута для сортировки
        
    Returns:
        Callable: Функция, возвращающая значение поля для сортировки
    """
    def sort_by_field(patient: Patient):
        return getattr(patient, field_name)
    return sort_by_field


def make_cost_discounter(percent: float) -> Callable[[Patient], Patient]:
    """
    Фабрика: создаёт функцию для применения скидки к стоимости лечения.
    
    Args:
        percent: Процент скидки
        
    Returns:
        Callable: Функция, применяющая скидку к пациенту
    """
    def apply_discount(patient: Patient) -> Patient:
        original_cost = patient.get_cost()
        discounted_cost = original_cost * (1 - percent / 100)
        # Создаём новый атрибут для демонстрации скидки
        patient.discounted_cost = discounted_cost
        return patient
    return apply_discount


# ============================================================================
# CALLABLE-ОБЪЕКТЫ (ПАТТЕРН СТРАТЕГИЯ)
# ============================================================================

class DiscountStrategy:
    """
    Стратегия расчета скидки на лечение.
    Реализует паттерн Стратегия через callable-объект.
    """
    
    def __init__(self, percent: float):
        """
        Инициализация стратегии скидки.
        
        Args:
            percent: Процент скидки (0-100)
        """
        self.percent = percent
        self.name = f"Скидка {percent}%"
    
    def __call__(self, patient: Patient) -> float:
        """
        Применяет скидку к стоимости лечения пациента.
        
        Args:
            patient: Объект пациента
            
        Returns:
            float: Стоимость лечения со скидкой
        """
        original_cost = patient.get_cost()
        return original_cost * (1 - self.percent / 100)
    
    def __str__(self) -> str:
        return self.name


class SortStrategy:
    """
    Стратегия сортировки пациентов.
    Реализует паттерн Стратегия через callable-объект.
    """
    
    def __init__(self, key_func: Callable, reverse: bool = False, name: str = "Стратегия сортировки"):
        """
        Инициализация стратегии сортировки.
        
        Args:
            key_func: Функция для получения ключа сортировки
            reverse: Сортировать в обратном порядке
            name: Название стратегии
        """
        self.key_func = key_func
        self.reverse = reverse
        self.name = name
    
    def __call__(self, items: list) -> list:
        """
        Сортирует список объектов.
        
        Args:
            items: Список объектов для сортировки
            
        Returns:
            list: Отсортированный список
        """
        return sorted(items, key=self.key_func, reverse=self.reverse)
    
    def __str__(self) -> str:
        return self.name


class ReportStrategy:
    """
    Стратегия формирования отчета о пациентах.
    Реализует паттерн Стратегия через callable-объект.
    """
    
    def __init__(self, format_type: str = "simple"):
        """
        Инициализация стратегии отчета.
        
        Args:
            format_type: Тип формата ("simple", "detailed", "csv")
        """
        self.format_type = format_type
    
    def __call__(self, patients: list) -> str:
        """
        Формирует отчет о пациентах.
        
        Args:
            patients: Список пациентов
            
        Returns:
            str: Отчет в выбранном формате
        """
        if self.format_type == "simple":
            return self._simple_report(patients)
        elif self.format_type == "detailed":
            return self._detailed_report(patients)
        elif self.format_type == "csv":
            return self._csv_report(patients)
        return self._simple_report(patients)
    
    def _simple_report(self, patients: list) -> str:
        """Простой формат отчета."""
        lines = [f"Всего пациентов: {len(patients)}"]
        for p in patients[:5]:
            lines.append(f"  - {p.name} ({p.age} лет)")
        return "\n".join(lines)
    
    def _detailed_report(self, patients: list) -> str:
        """Детальный формат отчета."""
        lines = [f"ДЕТАЛЬНЫЙ ОТЧЕТ", "="*40]
        for i, p in enumerate(patients, 1):
            lines.append(f"{i}. {p.get_short_info()}")
        return "\n".join(lines)
    
    def _csv_report(self, patients: list) -> str:
        """CSV формат отчета."""
        lines = ["name,age,diagnosis,cost,type"]
        for p in patients:
            lines.append(f"{p.name},{p.age},{p.diagnosis},{p.get_cost()},{p.get_type()}")
        return "\n".join(lines)
    
    def __str__(self) -> str:
        return f"Стратегия отчета (формат: {self.format_type})"