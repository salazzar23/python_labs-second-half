"""
Классы Patient, Inpatient, Outpatient для ЛР-5
Предметная область: Медицина
"""

from datetime import datetime


class Patient:
    """Базовый класс пациента."""
    
    def __init__(self, patient_id: str, name: str, age: int, diagnosis: str, doctor: str):
        if age <= 0 or age >= 150:
            raise ValueError("Возраст должен быть от 1 до 149 лет")
        
        self.patient_id = patient_id
        self.name = name
        self.age = age
        self.diagnosis = diagnosis
        self.doctor = doctor
        self.last_visit = datetime.now()
    
    def __str__(self) -> str:
        return f"{self.patient_id}: {self.name}, {self.age} лет, {self.diagnosis}"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Patient):
            return False
        return self.patient_id == other.patient_id
    
    def get_short_info(self) -> str:
        return f"{self.name} ({self.age} лет) - {self.diagnosis}"
    
    def compare(self, other) -> int:
        if not isinstance(other, Patient):
            raise TypeError("Можно сравнивать только с Patient")
        if self.age < other.age:
            return -1
        elif self.age > other.age:
            return 1
        return 0
    
    def is_senior(self) -> bool:
        return self.age > 65
    
    def needs_urgent_care(self) -> bool:
        urgent = ["инфаркт", "инсульт", "аппендицит", "кровотечение"]
        return any(u in self.diagnosis.lower() for u in urgent)
    
    def get_cost(self) -> float:
        return 0.0
    
    def get_type(self) -> str:
        return "Обычный пациент"


class Inpatient(Patient):
    """Стационарный пациент."""
    
    def __init__(self, patient_id: str, name: str, age: int, diagnosis: str,
                 doctor: str, ward: str, admission_date: datetime):
        super().__init__(patient_id, name, age, diagnosis, doctor)
        self.ward = ward
        self.admission_date = admission_date
        self.discharged = False
    
    def __str__(self) -> str:
        status = "ВЫПИСАН" if self.discharged else "В СТАЦИОНАРЕ"
        return f"{super().__str__()} | палата {self.ward}, {status}"
    
    def get_short_info(self) -> str:
        return f"[СТАЦИОНАР] {self.name}, палата {self.ward}, {self.diagnosis}, дней: {self.get_days()}"
    
    def compare(self, other) -> int:
        if isinstance(other, Inpatient):
            if self.get_days() < other.get_days():
                return -1
            elif self.get_days() > other.get_days():
                return 1
            return 0
        return super().compare(other)
    
    def discharge(self) -> None:
        if not self.discharged:
            self.discharged = True
            print(f"      -> {self.name} выписан")
    
    def get_days(self) -> int:
        if self.discharged:
            return 0
        days = (datetime.now() - self.admission_date).days
        return days if days > 0 else 1
    
    def get_cost(self) -> float:
        return 5000 * self.get_days()
    
    def get_type(self) -> str:
        return "Стационарный пациент"


class Outpatient(Patient):
    """Амбулаторный пациент."""
    
    def __init__(self, patient_id: str, name: str, age: int, diagnosis: str,
                 doctor: str, next_appointment: datetime):
        super().__init__(patient_id, name, age, diagnosis, doctor)
        self.next_appointment = next_appointment
        self.visits = 1
    
    def __str__(self) -> str:
        date_str = self.next_appointment.strftime("%d.%m.%Y")
        return f"{super().__str__()} | след. приём: {date_str}, визитов: {self.visits}"
    
    def get_short_info(self) -> str:
        return f"[АМБУЛАТОРНО] {self.name}, {self.diagnosis}, визитов: {self.visits}"
    
    def compare(self, other) -> int:
        if isinstance(other, Outpatient):
            if self.visits < other.visits:
                return -1
            elif self.visits > other.visits:
                return 1
            return 0
        return super().compare(other)
    
    def add_visit(self) -> None:
        self.visits += 1
        print(f"      -> {self.name} визит №{self.visits}")
    
    def get_cost(self) -> float:
        return 1500 * self.visits
    
    def get_type(self) -> str:
        return "Амбулаторный пациент"