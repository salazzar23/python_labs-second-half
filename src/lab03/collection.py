from base import Patient


class PatientCollection:
    def __init__(self):
        self.items = []
    
    def add(self, patient):
        if not isinstance(patient, Patient):
            raise TypeError("Можно только Patient")
        for p in self.items:
            if p.patient_id == patient.patient_id:
                print(f"      Ошибка: дубликат {patient.patient_id}")
                return False
        self.items.append(patient)
        print(f"      + {patient.name}")
        return True
    
    def remove(self, patient):
        if patient in self.items:
            self.items.remove(patient)
            print(f"      - {patient.name}")
            return True
        print(f"      Ошибка: {patient.name} не найден")
        return False
    
    def remove_at(self, index):
        if 0 <= index < len(self.items):
            removed = self.items.pop(index)
            print(f"      - Удалён по индексу {index}: {removed.name}")
            return removed
        print(f"      Ошибка: индекс {index} вне диапазона")
        return None
    
    def get_all(self):
        return self.items.copy()
    
    def find_by_id(self, patient_id):
        """Поиск пациента по ID."""
        for p in self.items:
            if p.patient_id == patient_id:
                print(f"      Найден: {p.name}")
                return p
        print(f"      Пациент {patient_id} не найден")
        return None
    
    def find_by_name(self, name):
        """Поиск пациентов по имени (частичное совпадение)."""
        results = [p for p in self.items if name.lower() in p.name.lower()]
        print(f"      Найдено {len(results)} пациентов с именем '{name}'")
        for p in results:
            print(f"        - {p.name}")
        return results
    
    def find_by_diagnosis(self, diagnosis):
        """Поиск пациентов по диагнозу."""
        results = [p for p in self.items if diagnosis.lower() in p.diagnosis.lower()]
        print(f"      Найдено {len(results)} пациентов с диагнозом '{diagnosis}'")
        for p in results:
            print(f"        - {p.name}: {p.diagnosis}")
        return results
    
    def __len__(self):
        return len(self.items)
    
    def __iter__(self):
        return iter(self.items)
    
    def __contains__(self, patient):
        return patient in self.items
    
    def __getitem__(self, index):
        if isinstance(index, slice):
            return self.items[index]
        if isinstance(index, int):
            if index < 0:
                index = len(self.items) + index
            if 0 <= index < len(self.items):
                return self.items[index]
            raise IndexError(f"Индекс {index} вне диапазона")
        raise TypeError("Индекс должен быть целым числом")
    
    def sort_by_age(self, reverse=False):
        """Сортировка по возрасту."""
        new_col = PatientCollection()
        new_col.items = sorted(self.items, key=lambda p: p.age, reverse=reverse)
        return new_col
    
    def sort_by_name(self, reverse=False):
        """Сортировка по имени."""
        new_col = PatientCollection()
        new_col.items = sorted(self.items, key=lambda p: p.name, reverse=reverse)
        return new_col
    
    def get_seniors(self):
        """Получить пожилых пациентов (старше 65 лет)."""
        new_col = PatientCollection()
        new_col.items = [p for p in self.items if p.is_senior()]
        return new_col
    
    def get_urgent(self):
        """Получить пациентов, нуждающихся в срочной помощи."""
        new_col = PatientCollection()
        new_col.items = [p for p in self.items if p.needs_urgent_care()]
        return new_col
    
    def get_inpatients(self):
        """Получить только стационарных пациентов."""
        from models import Inpatient
        new_col = PatientCollection()
        new_col.items = [p for p in self.items if isinstance(p, Inpatient)]
        return new_col
    
    def get_outpatients(self):
        """Получить только амбулаторных пациентов."""
        from models import Outpatient
        new_col = PatientCollection()
        new_col.items = [p for p in self.items if isinstance(p, Outpatient)]
        return new_col
    
    def print_all(self):
        if not self.items:
            print("      Коллекция пуста")
            return
        print(f"\n      Всего пациентов: {len(self.items)}")
        print("      " + "-"*40)
        for i, p in enumerate(self.items):
            print(f"      [{i}] {p}")
        print()