"""
Бизнес-логика приложения
"""

from typing import List, Optional, Callable
from datetime import datetime
from models import Patient, Inpatient, Outpatient
from collection import PatientCollection
from exceptions import PatientNotFoundError, DuplicatePatientError, InvalidAgeError


class PatientApp:
    """Основной класс приложения для управления пациентами."""
    
    def __init__(self, collection: PatientCollection = None):
        """Инициализация приложения."""
        self.collection = collection if collection else PatientCollection()
    
    def add_patient(self, patient_id: str, name: str, age: int,
                    diagnosis: str, doctor: str) -> bool:
        """
        Добавить нового пациента.
        
        Args:
            patient_id: уникальный ID
            name: имя пациента
            age: возраст
            diagnosis: диагноз
            doctor: врач
            
        Returns:
            bool: успех операции
            
        Raises:
            InvalidAgeError: некорректный возраст
            DuplicatePatientError: дубликат ID
        """
        if age <= 0 or age >= 150:
            raise InvalidAgeError(f"Возраст {age} должен быть от 1 до 149 лет")
        
        try:
            return self.collection.add(Patient(patient_id, name, age, diagnosis, doctor))
        except Exception as e:
            raise DuplicatePatientError(f"Пациент с ID {patient_id} уже существует")
    
    def add_inpatient(self, patient_id: str, name: str, age: int,
                      diagnosis: str, doctor: str, ward: str) -> bool:
        """Добавить стационарного пациента."""
        if age <= 0 or age >= 150:
            raise InvalidAgeError(f"Возраст {age} должен быть от 1 до 149 лет")
        
        patient = Inpatient(patient_id, name, age, diagnosis, doctor, ward, datetime.now())
        return self.collection.add(patient)
    
    def add_outpatient(self, patient_id: str, name: str, age: int,
                       diagnosis: str, doctor: str, next_days: int) -> bool:
        """Добавить амбулаторного пациента."""
        if age <= 0 or age >= 150:
            raise InvalidAgeError(f"Возраст {age} должен быть от 1 до 149 лет")
        
        from datetime import timedelta
        next_date = datetime.now() + timedelta(days=next_days)
        patient = Outpatient(patient_id, name, age, diagnosis, doctor, next_date)
        return self.collection.add(patient)
    
    def remove_patient(self, patient_id: str, confirm: bool = False) -> bool:
        """
        Удалить пациента по ID.
        
        Args:
            patient_id: ID пациента
            confirm: подтверждение удаления
            
        Returns:
            bool: успех операции
            
        Raises:
            PatientNotFoundError: пациент не найден
        """
        patient = self.find_by_id(patient_id)
        if not patient:
            raise PatientNotFoundError(f"Пациент с ID {patient_id} не найден")
        
        if not confirm:
            return False
        
        return self.collection.remove(patient)
    
    def find_by_id(self, patient_id: str) -> Optional[Patient]:
        """Найти пациента по ID."""
        return self.collection.find_by_id(patient_id)
    
    def find_by_name(self, name: str) -> List[Patient]:
        """Найти пациентов по имени."""
        return self.collection.find_by_name(name)
    
    def get_all_patients(self) -> List[Patient]:
        """Получить всех пациентов."""
        return self.collection.get_all()
    
    def get_sorted_by_name(self) -> List[Patient]:
        """Сортировка по имени."""
        return self.collection.sort_by_name().get_all()
    
    def get_sorted_by_age(self, reverse: bool = False) -> List[Patient]:
        """Сортировка по возрасту."""
        return self.collection.sort_by_age(reverse).get_all()
    
    def get_sorted_by_cost(self) -> List[Patient]:
        """Сортировка по стоимости лечения."""
        return sorted(self.collection.get_all(), key=lambda p: p.get_cost(), reverse=True)
    
    def filter_seniors(self) -> List[Patient]:
        """Фильтр: пожилые пациенты."""
        return [p for p in self.collection if p.is_senior()]
    
    def filter_urgent(self) -> List[Patient]:
        """Фильтр: срочная помощь."""
        return [p for p in self.collection if p.needs_urgent_care()]
    
    def filter_inpatients(self) -> List[Patient]:
        """Фильтр: стационарные пациенты."""
        return [p for p in self.collection if isinstance(p, Inpatient)]
    
    def filter_outpatients(self) -> List[Patient]:
        """Фильтр: амбулаторные пациенты."""
        return [p for p in self.collection if isinstance(p, Outpatient)]
    
    def get_statistics(self) -> dict:
        """Получить статистику по коллекции."""
        patients = self.collection.get_all()
        return {
            'total': len(patients),
            'inpatients': len([p for p in patients if isinstance(p, Inpatient)]),
            'outpatients': len([p for p in patients if isinstance(p, Outpatient)]),
            'seniors': len([p for p in patients if p.is_senior()]),
            'urgent': len([p for p in patients if p.needs_urgent_care()]),
            'total_cost': sum(p.get_cost() for p in patients)
        }
    
    def get_collection(self) -> PatientCollection:
        """Вернуть коллекцию (для сохранения)."""
        return self.collection