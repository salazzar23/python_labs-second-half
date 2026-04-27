from datetime import datetime

class Patient:
    def __init__(self, patient_id, name, age, diagnosis, doctor):
        self.patient_id = patient_id
        self.name = name
        self.age = age
        self.diagnosis = diagnosis
        self.doctor = doctor
        self.last_visit = datetime.now()
    
    def __str__(self):
        return f"{self.patient_id}: {self.name}, {self.age} лет, {self.diagnosis}"
    
    def __eq__(self, other):
        if not isinstance(other, Patient):
            return False
        return self.patient_id == other.patient_id
    
    def is_senior(self):
        return self.age > 65
    
    def needs_urgent_care(self):
        urgent = ["инфаркт", "инсульт", "аппендицит"]
        return any(u in self.diagnosis.lower() for u in urgent)
    
    def get_cost(self):
        return 0
    
    def get_type(self):
        return "Обычный"
    
    def get_info(self):
        return f"{self.name} ({self.age} лет)"