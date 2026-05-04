"""
Классы Patient, Inpatient, Outpatient с реализацией интерфейсов Printable и Comparable
Предметная область: Медицина
"""

from datetime import datetime
from interfaces import Printable, Comparable


class Patient(Printable, Comparable):
    """
    Базовый класс пациента.
    Реализует интерфейсы Printable и Comparable.
    """
    
    def __init__(self, patient_id: str, name: str, age: int, diagnosis: str, doctor: str):
        """
        Инициализация пациента.
        
        Args:
            patient_id: Уникальный идентификатор
            name: Полное имя
            age: Возраст
            diagnosis: Диагноз
            doctor: Специализация врача
        """
        if age <= 0 or age >= 150:
            raise ValueError("Возраст должен быть от 1 до 149 лет")
        
        self.patient_id = patient_id
        self.name = name
        self.age = age
        self.diagnosis = diagnosis
        self.doctor = doctor
        self.last_visit = datetime.now()
    
    def __str__(self) -> str:
        return f"{self.patient_id}: {self.name}, {self.age} лет, {self.diagnosis}, врач: {self.doctor}"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Patient):
            return False
        return self.patient_id == other.patient_id
    
    # ========== Реализация интерфейса Printable ==========
    def get_short_info(self) -> str:
        """Возвращает краткую информацию о пациенте."""
        return f"{self.name} ({self.age} лет) - {self.diagnosis}"
    
    # ========== Реализация интерфейса Comparable ==========
    def compare(self, other) -> int:
        """
        Сравнивает пациентов по возрасту.
        
        Returns:
            -1 если self.age < other.age
            0 если self.age == other.age
            1 если self.age > other.age
        """
        if not isinstance(other, Patient):
            raise TypeError("Можно сравнивать только с Patient")
        
        if self.age < other.age:
            return -1
        elif self.age > other.age:
            return 1
        else:
            return 0
    
    # ========== Бизнес-методы ==========
    def is_senior(self) -> bool:
        """Проверка, пожилой ли пациент (старше 65 лет)."""
        return self.age > 65
    
    def needs_urgent_care(self) -> bool:
        """Проверка необходимости срочной помощи."""
        urgent = ["инфаркт", "инсульт", "аппендицит", "кровотечение", "перитонит"]
        return any(u in self.diagnosis.lower() for u in urgent)
    
    def get_cost(self) -> float:
        """Стоимость лечения (базовая)."""
        return 0.0
    
    def get_type(self) -> str:
        """Тип пациента."""
        return "Обычный пациент"


class Inpatient(Patient):
    """
    Стационарный пациент (лежит в больнице).
    Реализует интерфейсы Printable и Comparable со своей спецификой.
    """
    
    def __init__(self, patient_id: str, name: str, age: int, diagnosis: str,
                 doctor: str, ward: str, admission_date: datetime):
        """
        Инициализация стационарного пациента.
        
        Args:
            ward: Номер палаты
            admission_date: Дата поступления
        """
        super().__init__(patient_id, name, age, diagnosis, doctor)
        self.ward = ward
        self.admission_date = admission_date
        self.discharged = False
        self.discharge_date = None
    
    def __str__(self) -> str:
        status = "ВЫПИСАН" if self.discharged else "В СТАЦИОНАРЕ"
        admit_str = self.admission_date.strftime("%d.%m.%Y")
        return f"{super().__str__()} | палата {self.ward}, поступление: {admit_str}, {status}"
    
    # ========== Переопределение интерфейса Printable ==========
    def get_short_info(self) -> str:
        """Возвращает краткую информацию о стационарном пациенте."""
        return f"[СТАЦИОНАР] {self.name}, палата {self.ward}, {self.diagnosis}, дней: {self.get_days()}"
    
    # ========== Переопределение интерфейса Comparable ==========
    def compare(self, other) -> int:
        """
        Сравнивает стационарных пациентов по количеству дней в стационаре.
        Если другой объект не Inpatient, использует сравнение по возрасту.
        """
        if isinstance(other, Inpatient):
            if self.get_days() < other.get_days():
                return -1
            elif self.get_days() > other.get_days():
                return 1
            else:
                return 0
        else:
            return super().compare(other)
    
    # ========== Специфические методы ==========
    def discharge(self) -> None:
        """Выписать пациента из стационара."""
        if not self.discharged:
            self.discharged = True
            self.discharge_date = datetime.now()
            print(f"      -> {self.name} выписан из стационара")
    
    def get_days(self) -> int:
        """Количество дней в стационаре."""
        if self.discharged and self.discharge_date:
            days = (self.discharge_date - self.admission_date).days
        else:
            days = (datetime.now() - self.admission_date).days
        return max(days, 1)
    
    # ========== Переопределение бизнес-методов ==========
    def get_cost(self) -> float:
        """Стоимость лечения: 5000 руб. в день."""
        return 5000 * self.get_days()
    
    def get_type(self) -> str:
        return "Стационарный пациент"


class Outpatient(Patient):
    """
    Амбулаторный пациент (приходит на приёмы).
    Реализует интерфейсы Printable и Comparable со своей спецификой.
    """
    
    def __init__(self, patient_id: str, name: str, age: int, diagnosis: str,
                 doctor: str, next_appointment: datetime):
        """
        Инициализация амбулаторного пациента.
        
        Args:
            next_appointment: Дата следующего приёма
        """
        super().__init__(patient_id, name, age, diagnosis, doctor)
        self.next_appointment = next_appointment
        self.visits = 1
        self.visit_history = [datetime.now()]
    
    def __str__(self) -> str:
        date_str = self.next_appointment.strftime("%d.%m.%Y")
        return f"{super().__str__()} | след. приём: {date_str}, визитов: {self.visits}"
    
    # ========== Переопределение интерфейса Printable ==========
    def get_short_info(self) -> str:
        """Возвращает краткую информацию об амбулаторном пациенте."""
        return f"[АМБУЛАТОРНО] {self.name}, {self.diagnosis}, визитов: {self.visits}"
    
    # ========== Переопределение интерфейса Comparable ==========
    def compare(self, other) -> int:
        """
        Сравнивает амбулаторных пациентов по количеству визитов.
        Если другой объект не Outpatient, использует сравнение по возрасту.
        """
        if isinstance(other, Outpatient):
            if self.visits < other.visits:
                return -1
            elif self.visits > other.visits:
                return 1
            else:
                return 0
        else:
            return super().compare(other)
    
    # ========== Специфические методы ==========
    def add_visit(self) -> None:
        """Зарегистрировать новый визит."""
        self.visits += 1
        self.visit_history.append(datetime.now())
        print(f"      -> {self.name} визит №{self.visits}")
    
    def reschedule(self, new_date: datetime) -> None:
        """Перенести дату следующего приёма."""
        old_date = self.next_appointment
        self.next_appointment = new_date
        print(f"      -> Приём для {self.name} перенесён с {old_date.strftime('%d.%m.%Y')} на {new_date.strftime('%d.%m.%Y')}")
    
    # ========== Переопределение бизнес-методов ==========
    def get_cost(self) -> float:
        """Стоимость лечения: 1500 руб. за визит."""
        return 1500 * self.visits
    
    def get_type(self) -> str:
        return "Амбулаторный пациент"