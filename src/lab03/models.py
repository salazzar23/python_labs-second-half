"""
Производные классы для иерархии пациентов.
Inpatient - стационарный пациент
Outpatient - амбулаторный пациент
"""

from datetime import datetime
from base import Patient


class Inpatient(Patient):
    """
    Стационарный пациент (находится в больнице).
    
    Дополнительные атрибуты:
        ward_number (str): Номер палаты
        admission_date (datetime): Дата госпитализации
        expected_discharge_date (datetime): Ожидаемая дата выписки
    
    Дополнительные методы:
        discharge(): Выписать пациента
        get_hospitalization_days(): Количество дней в стационаре
    """
    
    def __init__(self, patient_id: str, name: str, age: int,
                 diagnosis: str, last_appointment_date: datetime,
                 doctor_specialization: str, ward_number: str,
                 admission_date: datetime, expected_discharge_date: datetime):
        """
        Инициализация стационарного пациента.
        Использует super() для вызова конструктора базового класса.
        """
        super().__init__(patient_id, name, age, diagnosis, 
                        last_appointment_date, doctor_specialization)
        self.ward_number = ward_number
        self.admission_date = admission_date
        self.expected_discharge_date = expected_discharge_date
        self.is_discharged = False
    
    def __str__(self) -> str:
        """Переопределённый метод вывода информации."""
        base_str = super().__str__()
        status = "ВЫПИСАН" if self.is_discharged else "В СТАЦИОНАРЕ"
        return (f"{base_str}\n  [СТАЦИОНАР] Палата: {self.ward_number}, "
                f"Поступление: {self.admission_date.strftime('%d.%m.%Y')}, "
                f"Статус: {status}")
    
    def discharge(self) -> None:
        """Выписать пациента из стационара."""
        if not self.is_discharged:
            self.is_discharged = True
            print(f"Пациент {self.name} выписан из стационара")
        else:
            print(f"Пациент {self.name} уже выписан")
    
    def get_hospitalization_days(self) -> int:
        """Рассчитать количество дней в стационаре."""
        if self.is_discharged:
            return 0
        today = datetime.now()
        days = (today - self.admission_date).days
        return max(days, 0)
    
    def get_treatment_cost(self) -> float:
        """
        Переопределённый метод расчёта стоимости лечения.
        Для стационарного пациента: 5000 руб. в день + стоимость процедур.
        """
        days = self.get_hospitalization_days()
        if days == 0:
            days = 1
        base_cost = 5000 * days
        # Дополнительная стоимость в зависимости от диагноза
        if "инфаркт" in self.diagnosis.lower() or "инсульт" in self.diagnosis.lower():
            base_cost += 20000
        return base_cost
    
    def get_patient_type(self) -> str:
        """Вернуть тип пациента (полиморфизм)."""
        return "Стационарный пациент"
    
    def display_info(self) -> str:
        """Переопределённый интерфейс вывода информации."""
        return f"[СТАЦИОНАР] {self.name} - {self.diagnosis} (палата {self.ward_number})"


class Outpatient(Patient):
    """
    Амбулаторный пациент (приходит на приёмы).
    
    Дополнительные атрибуты:
        next_appointment_date (datetime): Дата следующего приёма
        requires_referral (bool): Требуется ли направление
    
    Дополнительные методы:
        reschedule_appointment(): Перенести приём
        needs_referral_check(): Проверка необходимости направления
    """
    
    def __init__(self, patient_id: str, name: str, age: int,
                 diagnosis: str, last_appointment_date: datetime,
                 doctor_specialization: str, next_appointment_date: datetime,
                 requires_referral: bool = False):
        """
        Инициализация амбулаторного пациента.
        Использует super() для вызова конструктора базового класса.
        """
        super().__init__(patient_id, name, age, diagnosis,
                        last_appointment_date, doctor_specialization)
        self.next_appointment_date = next_appointment_date
        self.requires_referral = requires_referral
        self.visit_count = 1
    
    def __str__(self) -> str:
        """Переопределённый метод вывода информации."""
        base_str = super().__str__()
        referral_status = "Требуется направление" if self.requires_referral else "Направление не требуется"
        next_date = self.next_appointment_date.strftime('%d.%m.%Y') if self.next_appointment_date else "Не назначен"
        return (f"{base_str}\n  [АМБУЛАТОРНО] Следующий приём: {next_date}, "
                f"Визитов: {self.visit_count}, {referral_status}")
    
    def reschedule_appointment(self, new_date: datetime) -> None:
        """Перенести дату следующего приёма."""
        old_date = self.next_appointment_date
        self.next_appointment_date = new_date
        print(f"Приём для {self.name} перенесён с {old_date.strftime('%d.%m.%Y')} "
              f"на {new_date.strftime('%d.%m.%Y')}")
    
    def register_visit(self) -> None:
        """Зарегистрировать посещение."""
        self.visit_count += 1
        print(f"Зарегистрирован визит {self.visit_count} для {self.name}")
    
    def needs_referral_check(self) -> bool:
        """Проверить, нужно ли пациенту направление к узкому специалисту."""
        return self.requires_referral
    
    def get_treatment_cost(self) -> float:
        """
        Переопределённый метод расчёта стоимости лечения.
        Для амбулаторного пациента: стоимость за визит + консультации.
        """
        base_cost = 1500 * self.visit_count
        # Дополнительная стоимость за направление
        if self.requires_referral:
            base_cost += 800
        return base_cost
    
    def get_patient_type(self) -> str:
        """Вернуть тип пациента (полиморфизм)."""
        return "Амбулаторный пациент"
    
    def display_info(self) -> str:
        """Переопределённый интерфейс вывода информации."""
        return f"[АМБУЛАТОРНО] {self.name} - {self.diagnosis} (визитов: {self.visit_count})"