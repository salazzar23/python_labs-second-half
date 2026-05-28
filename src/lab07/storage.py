"""
Сохранение и загрузка данных в JSON
"""

import json
from datetime import datetime
from typing import List
from models import Patient, Inpatient, Outpatient


def save(collection, filepath: str = "patients.json") -> None:
    """
    Сохранить коллекцию пациентов в JSON-файл.
    
    Args:
        collection: PatientCollection
        filepath: путь к файлу
    """
    data = []
    for p in collection.get_all():
        item = {
            'type': p.get_type(),
            'patient_id': p.patient_id,
            'name': p.name,
            'age': p.age,
            'diagnosis': p.diagnosis,
            'doctor': p.doctor,
            'last_visit': p.last_visit.isoformat()
        }
        
        if isinstance(p, Inpatient):
            item['ward'] = p.ward
            item['admission_date'] = p.admission_date.isoformat()
            item['discharged'] = p.discharged
        
        if isinstance(p, Outpatient):
            item['next_appointment'] = p.next_appointment.isoformat()
            item['visits'] = p.visits
        
        data.append(item)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"      Сохранено {len(data)} пациентов в {filepath}")


def load(filepath: str = "patients.json") -> List:
    """
    Загрузить пациентов из JSON-файла.
    
    Args:
        filepath: путь к файлу
        
    Returns:
        List[Patient]: список загруженных пациентов
    """
    patients = []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"      Файл {filepath} не найден. Начинаем с пустой коллекции.")
        return []
    
    for item in data:
        try:
            patient_type = item.get('type', 'Обычный пациент')
            last_visit = datetime.fromisoformat(item['last_visit'])
            
            if patient_type == 'Стационарный пациент':
                admission_date = datetime.fromisoformat(item['admission_date'])
                patient = Inpatient(
                    item['patient_id'], item['name'], item['age'],
                    item['diagnosis'], item['doctor'], item['ward'],
                    admission_date
                )
                if item.get('discharged', False):
                    patient.discharge()
            elif patient_type == 'Амбулаторный пациент':
                next_appointment = datetime.fromisoformat(item['next_appointment'])
                patient = Outpatient(
                    item['patient_id'], item['name'], item['age'],
                    item['diagnosis'], item['doctor'], next_appointment
                )
                patient.visits = item.get('visits', 1)
            else:
                patient = Patient(
                    item['patient_id'], item['name'], item['age'],
                    item['diagnosis'], item['doctor']
                )
                patient.last_visit = last_visit
            
            patients.append(patient)
        except Exception as e:
            print(f"      Ошибка загрузки пациента {item.get('name', '?')}: {e}")
    
    print(f"      Загружено {len(patients)} пациентов из {filepath}")
    return patients