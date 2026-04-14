from typing import List, Optional, Iterator
from model import Patient

class PatientCollection:
    def __init__(self):
        self._patients: List[Patient] = []
    
    def add(self, patient: Patient) -> bool:
        if not isinstance(patient, Patient):
            raise TypeError(f"Можно добавлять только объекты Patient")
        
        # Проверка на дубликат
        for p in self._patients:
            if p.patient_id == patient.patient_id:
                print(f"Ошибка: Пациент с ID {patient.patient_id} уже существует")
                return False
        
        self._patients.append(patient)
        print(f"Пациент {patient.name} добавлен")
        return True
    
    def remove(self, patient: Patient) -> bool:
        if patient in self._patients:
            self._patients.remove(patient)
            print(f"Пациент {patient.name} удалён")
            return True
        print("Ошибка: Пациент не найден")
        return False
    
    def get_all(self) -> List[Patient]:
        return self._patients.copy()
    
    def find_by_id(self, patient_id: str) -> Optional[Patient]:
        for patient in self._patients:
            if patient.patient_id == patient_id:
                print(f"Найден: {patient}")
                return patient
        print(f"Пациент с ID {patient_id} не найден")
        return None
    
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
    
    def print_all(self):
        if not self._patients:
            print("Коллекция пуста")
            return
        print(f"\nКоллекция пациентов (всего: {len(self._patients)})")
        for i, patient in enumerate(self._patients):
            print(f"[{i}] {patient}")
        print()