"""
Коллекция пациентов (из ЛР-2, адаптирована для ЛР-4)
Добавлены методы для фильтрации по интерфейсам
"""

from typing import List, Optional, Iterator
from interfaces import Printable, Comparable
from models import Patient


class PatientCollection:
    """
    Коллекция для хранения и управления пациентами.
    Поддерживает фильтрацию по интерфейсам Printable и Comparable.
    """
    
    def __init__(self):
        self._patients: List[Patient] = []
    
    def add(self, patient: Patient) -> bool:
        """Добавить пациента в коллекцию."""
        if not isinstance(patient, Patient):
            raise TypeError(f"Можно добавлять только Patient, получен {type(patient)}")
        
        for p in self._patients:
            if p.patient_id == patient.patient_id:
                print(f"      ОШИБКА: Пациент {patient.patient_id} уже существует")
                return False
        
        self._patients.append(patient)
        print(f"      + {patient.name}")
        return True
    
    def remove(self, patient: Patient) -> bool:
        """Удалить пациента из коллекции."""
        if patient in self._patients:
            self._patients.remove(patient)
            print(f"      - {patient.name}")
            return True
        print(f"      ОШИБКА: Пациент {patient.name} не найден")
        return False
    
    def remove_at(self, index: int) -> Optional[Patient]:
        """Удалить пациента по индексу."""
        if 0 <= index < len(self._patients):
            removed = self._patients.pop(index)
            print(f"      - Удалён по индексу {index}: {removed.name}")
            return removed
        print(f"      ОШИБКА: Индекс {index} вне диапазона")
        return None
    
    def get_all(self) -> List[Patient]:
        """Получить копию списка всех пациентов."""
        return self._patients.copy()
    
    def find_by_id(self, patient_id: str) -> Optional[Patient]:
        """Поиск пациента по ID."""
        for p in self._patients:
            if p.patient_id == patient_id:
                print(f"      Найден: {p.name}")
                return p
        print(f"      Пациент {patient_id} не найден")
        return None
    
    def find_by_name(self, name: str) -> List[Patient]:
        """Поиск пациентов по имени."""
        results = [p for p in self._patients if name.lower() in p.name.lower()]
        print(f"      Найдено {len(results)} пациентов с именем '{name}'")
        return results
    
    # ========== МЕТОДЫ ДЛЯ РАБОТЫ С ИНТЕРФЕЙСАМИ (ЛР-4) ==========
    
    def get_printable(self) -> List[Printable]:
        """
        Вернуть все объекты, реализующие интерфейс Printable.
        """
        return [p for p in self._patients if isinstance(p, Printable)]
    
    def get_comparable(self) -> List[Comparable]:
        """
        Вернуть все объекты, реализующие интерфейс Comparable.
        """
        return [p for p in self._patients if isinstance(p, Comparable)]
    
    # ========== МАГИЧЕСКИЕ МЕТОДЫ ==========
    
    def __len__(self) -> int:
        return len(self._patients)
    
    def __iter__(self) -> Iterator[Patient]:
        return iter(self._patients)
    
    def __getitem__(self, index):
        if isinstance(index, slice):
            return self._patients[index]
        if isinstance(index, int):
            if index < 0:
                index = len(self._patients) + index
            if 0 <= index < len(self._patients):
                return self._patients[index]
            raise IndexError(f"Индекс {index} вне диапазона")
        raise TypeError("Индекс должен быть целым числом")
    
    def __contains__(self, patient) -> bool:
        return patient in self._patients
    
    # ========== СОРТИРОВКА ==========
    
    def sort_by_age(self, reverse: bool = False) -> 'PatientCollection':
        """Сортировка по возрасту."""
        new_col = PatientCollection()
        new_col._patients = sorted(self._patients, key=lambda p: p.age, reverse=reverse)
        return new_col
    
    def sort_by_name(self, reverse: bool = False) -> 'PatientCollection':
        """Сортировка по имени."""
        new_col = PatientCollection()
        new_col._patients = sorted(self._patients, key=lambda p: p.name, reverse=reverse)
        return new_col
    
    # ========== ФИЛЬТРАЦИЯ ==========
    
    def get_seniors(self) -> 'PatientCollection':
        """Получить только пожилых пациентов."""
        new_col = PatientCollection()
        new_col._patients = [p for p in self._patients if p.is_senior()]
        return new_col
    
    def get_urgent(self) -> 'PatientCollection':
        """Получить пациентов, нуждающихся в срочной помощи."""
        new_col = PatientCollection()
        new_col._patients = [p for p in self._patients if p.needs_urgent_care()]
        return new_col
    
    def get_inpatients(self) -> 'PatientCollection':
        """Получить только стационарных пациентов."""
        new_col = PatientCollection()
        new_col._patients = [p for p in self._patients if isinstance(p, Inpatient)]
        return new_col
    
    def get_outpatients(self) -> 'PatientCollection':
        """Получить только амбулаторных пациентов."""
        new_col = PatientCollection()
        new_col._patients = [p for p in self._patients if isinstance(p, Outpatient)]
        return new_col
    
    def print_all(self) -> None:
        """Вывести всех пациентов."""
        if not self._patients:
            print("      Коллекция пуста")
            return
        print(f"\n      Всего пациентов: {len(self._patients)}")
        print("      " + "-"*40)
        for i, p in enumerate(self._patients):
            print(f"      [{i}] {p}")
        print()