from datetime import datetime
from base import Patient


class Inpatient(Patient):
    """Стационарный пациент."""
    
    def __init__(self, patient_id, name, age, diagnosis, doctor, ward, admission_date):
        super().__init__(patient_id, name, age, diagnosis, doctor)
        self.ward = ward
        self.admission = admission_date
        self.discharged = False
    
    def __str__(self):
        status = "ВЫПИСАН" if self.discharged else "В БОЛЬНИЦЕ"
        return f"{super().__str__()} | палата {self.ward}, {status}"
    
    def discharge(self):
        self.discharged = True
        print(f"      -> {self.name} выписан")
    
    def get_days(self):
        if self.discharged:
            return 0
        days = (datetime.now() - self.admission).days
        return days if days > 0 else 1
    
    def get_cost(self):
        return 5000 * self.get_days()
    
    def get_type(self):
        return "Стационарный"


class Outpatient(Patient):
    """Амбулаторный пациент."""
    
    def __init__(self, patient_id, name, age, diagnosis, doctor, next_date):
        super().__init__(patient_id, name, age, diagnosis, doctor)
        self.next_date = next_date
        self.visits = 1
    
    def __str__(self):
        date_str = self.next_date.strftime('%d.%m.%Y')
        return f"{super().__str__()} | след.приём: {date_str}, визитов: {self.visits}"
    
    def add_visit(self):
        self.visits += 1
        print(f"      -> {self.name} визит #{self.visits}")
    
    def get_cost(self):
        return 1500 * self.visits
    
    def get_type(self):
        return "Амбулаторный"