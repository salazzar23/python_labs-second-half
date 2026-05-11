"""
Классы Patient, Inpatient, Outpatient с аннотациями типов для ЛР-6
Предметная область: Медицина
"""

from datetime import datetime
from typing import Optional


class Patient:
    """Базовый класс пациента с аннотациями типов."""
    
    def __init__(self, patient_id: str, name: str, age: int, 
                 diagnosis: str, doctor: str) -> None:
        """
        Инициализация пациента.
        
        Args:
            patient_id: Уникальный идентификатор
            name: Полное имя
            age: Возраст (1-149 лет)
            diagnosis: Диагноз
            doctor: Специализация врача
        """
        if age <= 0 or age >= 150:
            raise ValueError("Возраст должен быть от 1 до 149 лет")
        
        self.patient_id: str = patient_id
        self.name: str = name
        self.age: int = age
        self.diagnosis: str = diagnosis
        self.doctor: str = doctor
        self.last_visit: datetime = datetime.now()
    
    def __str__(self) -> str:
        return f"{self.patient_id}: {self.name}, {self.age} лет, {self.diagnosis}"
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Patient):
            return False
        return self.patient_id == other.patient_id
    
    def get_short_info(self) -> str:
        """Возвращает краткую информацию о пациенте."""
        return f"{self.name} ({self.age} лет) - {self.diagnosis}"
    
    def display(self) -> str:
        """Метод для протокола Displayable."""
        return self.get_short_info()
    
    def get_score(self) -> float:
        """Метод для протокола Scorable. Возвращает приоритет лечения."""
        if self.needs_urgent_care():
            return 100.0
        elif self.is_senior():
            return 50.0
        else:
            return 10.0
    
    def compare(self, other: 'Patient') -> int:
        """Сравнение пациентов по возрасту."""
        if self.age < other.age:
            return -1
        elif self.age > other.age:
            return 1
        return 0
    
    def is_senior(self) -> bool:
        """Проверка, пожилой ли пациент (старше 65 лет)."""
        return self.age > 65
    
    def needs_urgent_care(self) -> bool:
        """Проверка необходимости срочной помощи."""
        urgent: list[str] = ["инфаркт", "инсульт", "аппендицит", "кровотечение"]
        return any(u in self.diagnosis.lower() for u in urgent)
    
    def get_cost(self) -> float:
        """Стоимость лечения."""
        return 0.0
    
    def get_type(self) -> str:
        """Тип пациента."""
        return "Обычный пациент"


class Inpatient(Patient):
    """Стационарный пациент."""
    
    def __init__(self, patient_id: str, name: str, age: int, diagnosis: str,
                 doctor: str, ward: str, admission_date: datetime) -> None:
        super().__init__(patient_id, name, age, diagnosis, doctor)
        self.ward: str = ward
        self.admission_date: datetime = admission_date
        self.discharged: bool = False
    
    def __str__(self) -> str:
        status: str = "ВЫПИСАН" if self.discharged else "В СТАЦИОНАРЕ"
        return f"{super().__str__()} | палата {self.ward}, {status}"
    
    def get_short_info(self) -> str:
        return f"[СТАЦИОНАР] {self.name}, палата {self.ward}, {self.diagnosis}, дней: {self.get_days()}"
    
    def display(self) -> str:
        """Метод для протокола Displayable."""
        return self.get_short_info()
    
    def get_score(self) -> float:
        """Метод для протокола Scorable. Приоритет выше у срочных."""
        if self.needs_urgent_care():
            return 200.0
        return 100.0 + self.get_days()
    
    def discharge(self) -> None:
        if not self.discharged:
            self.discharged = True
            print(f"      -> {self.name} выписан")
    
    def get_days(self) -> int:
        if self.discharged:
            return 0
        days: int = (datetime.now() - self.admission_date).days
        return days if days > 0 else 1
    
    def get_cost(self) -> float:
        return 5000.0 * self.get_days()
    
    def get_type(self) -> str:
        return "Стационарный пациент"


class Outpatient(Patient):
    """Амбулаторный пациент."""
    
    def __init__(self, patient_id: str, name: str, age: int, diagnosis: str,
                 doctor: str, next_appointment: datetime) -> None:
        super().__init__(patient_id, name, age, diagnosis, doctor)
        self.next_appointment: datetime = next_appointment
        self.visits: int = 1
    
    def __str__(self) -> str:
        date_str: str = self.next_appointment.strftime("%d.%m.%Y")
        return f"{super().__str__()} | след. приём: {date_str}, визитов: {self.visits}"
    
    def get_short_info(self) -> str:
        return f"[АМБУЛАТОРНО] {self.name}, {self.diagnosis}, визитов: {self.visits}"
    
    def display(self) -> str:
        """Метод для протокола Displayable."""
        return self.get_short_info()
    
    def get_score(self) -> float:
        """Метод для протокола Scorable."""
        if self.needs_urgent_care():
            return 150.0
        return 50.0 + self.visits * 10
    
    def add_visit(self) -> None:
        self.visits += 1
        print(f"      -> {self.name} визит №{self.visits}")
    
    def get_cost(self) -> float:
        return 1500.0 * self.visits
    
    def get_type(self) -> str:
        return "Амбулаторный пациент"