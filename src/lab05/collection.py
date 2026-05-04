"""
Коллекция пациентов с функциональными методами для ЛР-5
Поддерживает сортировку, фильтрацию и применение функций
"""

from typing import List, Optional, Iterator, Callable, Any
from models import Patient


class PatientCollection:
    """Коллекция для хранения и управления пациентами с функциональными методами."""
    
    def __init__(self):
        self._patients: List[Patient] = []
    
    def add(self, patient: Patient) -> bool:
        """Добавить пациента в коллекцию."""
        if not isinstance(patient, Patient):
            raise TypeError(f"Можно добавлять только Patient")
        
        for p in self._patients:
            if p.patient_id == patient.patient_id:
                print(f"      ОШИБКА: Дубликат {patient.patient_id}")
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
        return False
    
    # ========== ФУНКЦИОНАЛЬНЫЕ МЕТОДЫ (ЛР-5) ==========
    
    def sort_by(self, key_func: Callable[[Patient], Any], reverse: bool = False) -> 'PatientCollection':
        """
        Сортирует коллекцию по переданной функции-ключу.
        
        Args:
            key_func: Функция для получения ключа сортировки
            reverse: Сортировать в обратном порядке
            
        Returns:
            PatientCollection: Новая отсортированная коллекция
        """
        new_collection = PatientCollection()
        new_collection._patients = sorted(self._patients, key=key_func, reverse=reverse)
        return new_collection
    
    def filter_by(self, predicate: Callable[[Patient], bool]) -> 'PatientCollection':
        """
        Фильтрует коллекцию по переданному предикату.
        
        Args:
            predicate: Функция-предикат для фильтрации
            
        Returns:
            PatientCollection: Новая отфильтрованная коллекция
        """
        new_collection = PatientCollection()
        new_collection._patients = [p for p in self._patients if predicate(p)]
        return new_collection
    
    def apply(self, func: Callable[[Patient], Any]) -> 'PatientCollection':
        """
        Применяет функцию ко всем элементам коллекции.
        
        Args:
            func: Функция для применения к каждому пациенту
            
        Returns:
            PatientCollection: Текущая коллекция (для цепочек вызовов)
        """
        for patient in self._patients:
            func(patient)
        return self
    
    def map_to(self, func: Callable[[Patient], Any]) -> List[Any]:
        """
        Применяет функцию к элементам и возвращает список результатов.
        
        Args:
            func: Функция для преобразования
            
        Returns:
            List[Any]: Список результатов применения функции
        """
        return list(map(func, self._patients))
    
    def chain(self,
              filter_pred: Optional[Callable[[Patient], bool]] = None,
              sort_key: Optional[Callable[[Patient], Any]] = None,
              sort_reverse: bool = False,
              apply_func: Optional[Callable[[Patient], Any]] = None) -> 'PatientCollection':
        """
        Цепочка операций: фильтр → сортировка → применение.
        
        Args:
            filter_pred: Функция-предикат для фильтрации
            sort_key: Функция-ключ для сортировки
            sort_reverse: Сортировать в обратном порядке
            apply_func: Функция для применения к каждому элементу
            
        Returns:
            PatientCollection: Результирующая коллекция
        """
        result = self
        
        if filter_pred is not None:
            result = result.filter_by(filter_pred)
        
        if sort_key is not None:
            result = result.sort_by(sort_key, sort_reverse)
        
        if apply_func is not None:
            result.apply(apply_func)
        
        return result
    
    # ========== ОСНОВНЫЕ МЕТОДЫ ==========
    
    def get_all(self) -> List[Patient]:
        return self._patients.copy()
    
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
            return self._patients[index]
        raise TypeError("Индекс должен быть целым числом")
    
    def print_all(self, title: str = "Все пациенты") -> None:
        """Вывести всех пациентов."""
        if not self._patients:
            print("      Коллекция пуста")
            return
        print(f"\n      {title} ({len(self._patients)}):")
        print("      " + "-"*40)
        for i, p in enumerate(self._patients):
            print(f"      {i+1}. {p.get_short_info()} | Стоимость: {p.get_cost()} руб.")
        print()