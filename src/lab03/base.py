"""
Базовый класс Patient для иерархии медицинских пациентов.
"""

from datetime import datetime
from typing import Optional


class Patient:
    """
    Базовый класс, представляющий пациента в медицинской системе.
    
    Атрибуты:
        patient_id (str): Уникальный идентификатор пациента
        name (str): Полное имя пациента
        age (int): Возраст пациента
        diagnosis (str): Диагноз
        last_appointment_date (datetime): Дата последнего приёма
        doctor_specialization (str): Специализация лечащего врача
    """
    
    def __init__(self, patient_id: str, name: str, age: int, 
                 diagnosis: str, last_appointment_date: datetime, 
                 doctor_specialization: str):
        """
        Инициализация нового пациента.
        """
        if age <= 0 or age >= 150:
            raise ValueError("Возраст должен быть между 1 и 149 годами")
        
        self.patient_id = patient_id
        self.name = name
        self.age = age
        self.diagnosis = diagnosis
        self.last_appointment_date = last_appointment_date
        self.doctor_specialization = doctor_specialization
    
    def __str__(self) -> str:
        """Строковое представление пациента."""
        date_str = self.last_appointment_date.strftime("%d.%m.%Y")
        return (f"Пациент #{self.patient_id}: {self.name}, {self.age} лет, "
                f"диагноз: {self.diagnosis}, врач: {self.doctor_specialization}, "
                f"последний приём: {date_str}")
    
    def __repr__(self) -> str:
        """Техническое представление пациента."""
        return (f"Patient(patient_id='{self.patient_id}', name='{self.name}', "
                f"age={self.age}, diagnosis='{self.diagnosis}')")
    
    def __eq__(self, other) -> bool:
        """Сравнение пациентов по уникальному идентификатору."""
        if not isinstance(other, Patient):
            return False
        return self.patient_id == other.patient_id
    
    def __hash__(self) -> int:
        """Хеш-функция на основе patient_id."""
        return hash(self.patient_id)
    
    def is_senior(self) -> bool:
        """Проверить, является ли пациент пожилым (старше 65 лет)."""
        return self.age > 65
    
    def needs_urgent_care(self) -> bool:
        """Проверить, нуждается ли пациент в срочной помощи."""
        urgent_diagnoses = ["инфаркт", "инсульт", "аппендицит", "кровотечение"]
        return any(diagnosis in self.diagnosis.lower() for diagnosis in urgent_diagnoses)
    
    def get_treatment_cost(self) -> float:
        """
        Базовый метод расчёта стоимости лечения.
        Переопределяется в дочерних классах (полиморфизм).
        """
        return 0.0
    
    def get_patient_type(self) -> str:
        """Вернуть тип пациента (для полиморфизма)."""
        return "Общий пациент"
    
    def display_info(self) -> str:
        """Общий интерфейс для вывода информации о пациенте."""
        return self.__str__()