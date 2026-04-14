from datetime import datetime

class Patient:
    def __init__(self, patient_id, name, age, diagnosis, last_appointment_date, doctor_specialization):
        if age <= 0 or age >= 150:
            raise ValueError("Возраст должен быть между 1 и 149 годами")
        
        self.patient_id = patient_id
        self.name = name
        self.age = age
        self.diagnosis = diagnosis
        self.last_appointment_date = last_appointment_date
        self.doctor_specialization = doctor_specialization
    
    def __str__(self):
        date_str = self.last_appointment_date.strftime("%d.%m.%Y")
        return f"Пациент #{self.patient_id}: {self.name}, {self.age} лет, диагноз: {self.diagnosis}"
    
    def __eq__(self, other):
        if not isinstance(other, Patient):
            return False
        return self.patient_id == other.patient_id
    
    def is_senior(self):
        return self.age > 65
    
    def needs_urgent_care(self):
        urgent_diagnoses = ["инфаркт", "инсульт", "аппендицит", "кровотечение"]
        return any(diagnosis in self.diagnosis.lower() for diagnosis in urgent_diagnoses)