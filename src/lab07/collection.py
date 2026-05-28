"""
Коллекция пациентов для ЛР-7
"""

from typing import List, Optional, Iterator
from models import Patient


class PatientCollection:
    """Коллекция для хранения и управления пациентами."""
    
    def __init__(self):
        self._items: List[Patient] = []
    
    def add(self, patient: Patient) -> bool:
        for p in self._items:
            if p.patient_id == patient.patient_id:
                print(f"      Ошибка: дубликат {patient.patient_id}")
                return False
        self._items.append(patient)
        print(f"      + {patient.name}")
        return True
    
    def remove(self, patient: Patient) -> bool:
        if patient in self._items:
            self._items.remove(patient)
            print(f"      - {patient.name}")
            return True
        return False
    
    def remove_at(self, index: int) -> Optional[Patient]:
        if 0 <= index < len(self._items):
            removed = self._items.pop(index)
            print(f"      - Удалён: {removed.name}")
            return removed
        return None
    
    def get_all(self) -> List[Patient]:
        return self._items.copy()
    
    def find_by_id(self, patient_id: str) -> Optional[Patient]:
        for p in self._items:
            if p.patient_id == patient_id:
                return p
        return None
    
    def find_by_name(self, name: str) -> List[Patient]:
        return [p for p in self._items if name.lower() in p.name.lower()]
    
    def sort_by_name(self):
        new = PatientCollection()
        new._items = sorted(self._items, key=lambda p: p.name)
        return new
    
    def sort_by_age(self, reverse=False):
        new = PatientCollection()
        new._items = sorted(self._items, key=lambda p: p.age, reverse=reverse)
        return new
    
    def __len__(self) -> int:
        return len(self._items)
    
    def __iter__(self):
        return iter(self._items)
    
    def __getitem__(self, index: int) -> Patient:
        if index < 0:
            index = len(self._items) + index
        return self._items[index]
    
    def print_all(self) -> None:
        if not self._items:
            print("      Коллекция пуста")
            return
        print(f"\n      Всего пациентов: {len(self._items)}")
        for i, p in enumerate(self._items):
            print(f"      [{i}] {p}")
        print()