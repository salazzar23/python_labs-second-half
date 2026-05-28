"""
CLI интерфейс пользователя
"""

from typing import List
from models import Patient, Inpatient, Outpatient
from app import PatientApp
from exceptions import PatientNotFoundError, DuplicatePatientError, InvalidAgeError


class PatientCLI:
    """Консольный интерфейс для работы с пациентами."""
    
    def __init__(self, app: PatientApp):
        """Инициализация CLI."""
        self.app = app
    
    def print_header(self, text: str) -> None:
        """Печать заголовка."""
        print("\n" + "="*60)
        print(f" {text}")
        print("="*60)
    
    def print_patient_table(self, patients: List[Patient], title: str = "Список пациентов") -> None:
        """Вывести таблицу пациентов."""
        if not patients:
            print(f"\n      {title}: пусто")
            return
        
        print(f"\n      {title} ({len(patients)}):")
        print("      " + "-"*56)
        print(f"      {'ID':<6} {'Имя':<20} {'Возраст':<8} {'Диагноз':<15}")
        print("      " + "-"*56)
        for p in patients:
            print(f"      {p.patient_id:<6} {p.name[:18]:<20} {p.age:<8} {p.diagnosis[:14]:<15}")
        print("      " + "-"*56)
    
    def print_patient_details(self, patient) -> None:
        """Вывести детальную информацию о пациенте."""
        if not patient:
            print("\n      Пациент не найден")
            return
        
        print("\n      " + "-"*40)
        print(f"      ID: {patient.patient_id}")
        print(f"      Имя: {patient.name}")
        print(f"      Возраст: {patient.age}")
        print(f"      Диагноз: {patient.diagnosis}")
        print(f"      Врач: {patient.doctor}")
        print(f"      Тип: {patient.get_type()}")
        print(f"      Стоимость лечения: {patient.get_cost()} руб.")
        
        if isinstance(patient, Inpatient):
            print(f"      Палата: {patient.ward}")
            print(f"      Дней в стационаре: {patient.get_days()}")
        if isinstance(patient, Outpatient):
            print(f"      Визитов: {patient.visits}")
            print(f"      Следующий приём: {patient.next_appointment.strftime('%d.%m.%Y')}")
        print("      " + "-"*40)
    
    def add_patient_flow(self) -> None:
        """Сценарий добавления обычного пациента."""
        self.print_header("ДОБАВЛЕНИЕ ПАЦИЕНТА")
        
        try:
            patient_id = input("   ID пациента: ").strip()
            name = input("   Имя: ").strip()
            age = int(input("   Возраст: ").strip())
            diagnosis = input("   Диагноз: ").strip()
            doctor = input("   Врач: ").strip()
            
            self.app.add_patient(patient_id, name, age, diagnosis, doctor)
            print(f"\n   Пациент {name} добавлен!")
            
        except ValueError:
            print("\n   Ошибка: возраст должен быть числом")
        except InvalidAgeError as e:
            print(f"\n   Ошибка: {e}")
        except DuplicatePatientError as e:
            print(f"\n   Ошибка: {e}")
    
    def add_inpatient_flow(self) -> None:
        """Сценарий добавления стационарного пациента."""
        self.print_header("ДОБАВЛЕНИЕ СТАЦИОНАРНОГО ПАЦИЕНТА")
        
        try:
            patient_id = input("   ID пациента: ").strip()
            name = input("   Имя: ").strip()
            age = int(input("   Возраст: ").strip())
            diagnosis = input("   Диагноз: ").strip()
            doctor = input("   Врач: ").strip()
            ward = input("   Номер палаты: ").strip()
            
            self.app.add_inpatient(patient_id, name, age, diagnosis, doctor, ward)
            print(f"\n   Стационарный пациент {name} добавлен в палату {ward}!")
            
        except ValueError:
            print("\n   Ошибка: возраст должен быть числом")
        except InvalidAgeError as e:
            print(f"\n   Ошибка: {e}")
        except DuplicatePatientError as e:
            print(f"\n   Ошибка: {e}")
    
    def add_outpatient_flow(self) -> None:
        """Сценарий добавления амбулаторного пациента."""
        self.print_header("ДОБАВЛЕНИЕ АМБУЛАТОРНОГО ПАЦИЕНТА")
        
        try:
            patient_id = input("   ID пациента: ").strip()
            name = input("   Имя: ").strip()
            age = int(input("   Возраст: ").strip())
            diagnosis = input("   Диагноз: ").strip()
            doctor = input("   Врач: ").strip()
            next_days = int(input("   Через сколько дней следующий приём: ").strip())
            
            self.app.add_outpatient(patient_id, name, age, diagnosis, doctor, next_days)
            print(f"\n   Амбулаторный пациент {name} добавлен!")
            
        except ValueError:
            print("\n   Ошибка: введите корректные числа")
        except InvalidAgeError as e:
            print(f"\n   Ошибка: {e}")
        except DuplicatePatientError as e:
            print(f"\n   Ошибка: {e}")
    
    def remove_patient_flow(self) -> None:
        """Сценарий удаления пациента с подтверждением."""
        self.print_header("УДАЛЕНИЕ ПАЦИЕНТА")
        
        patient_id = input("   ID пациента для удаления: ").strip()
        
        patient = self.app.find_by_id(patient_id)
        if not patient:
            print(f"\n   Пациент с ID {patient_id} не найден")
            return
        
        self.print_patient_details(patient)
        
        confirm = input(f"\n   Удалить пациента {patient.name}? (y/n): ").strip().lower()
        if confirm != 'y':
            print("\n   Удаление отменено")
            return
        
        try:
            self.app.remove_patient(patient_id, confirm=True)
            print(f"\n   Пациент {patient.name} удалён!")
        except PatientNotFoundError as e:
            print(f"\n   Ошибка: {e}")
    
    def find_patient_flow(self) -> None:
        """Сценарий поиска пациента."""
        self.print_header("ПОИСК ПАЦИЕНТА")
        
        print("\n   1. Поиск по ID")
        print("   2. Поиск по имени")
        
        choice = input("\n   Выберите тип поиска: ").strip()
        
        if choice == '1':
            patient_id = input("   ID пациента: ").strip()
            patient = self.app.find_by_id(patient_id)
            self.print_patient_details(patient)
        
        elif choice == '2':
            name = input("   Имя (частично): ").strip()
            results = self.app.find_by_name(name)
            self.print_patient_table(results, f"Результаты поиска по имени '{name}'")
        
        else:
            print("\n   Неверный выбор")
    
    def show_all_patients_flow(self) -> None:
        """Показать всех пациентов."""
        self.print_header("ВСЕ ПАЦИЕНТЫ")
        patients = self.app.get_all_patients()
        self.print_patient_table(patients, "Полный список")
        
        for p in patients[:3]:
            print(f"\n   {p}")
    
    def sort_patients_flow(self) -> None:
        """Сценарий сортировки."""
        self.print_header("СОРТИРОВКА")
        
        print("\n   1. По имени (А->Я)")
        print("   2. По возрасту (молодые->пожилые)")
        print("   3. По возрасту (пожилые->молодые)")
        print("   4. По стоимости лечения (дорогие->дешёвые)")
        
        choice = input("\n   Выберите сортировку: ").strip()
        
        if choice == '1':
            patients = self.app.get_sorted_by_name()
            self.print_patient_table(patients, "Сортировка по имени")
        elif choice == '2':
            patients = self.app.get_sorted_by_age()
            self.print_patient_table(patients, "Сортировка по возрасту (молодые->пожилые)")
        elif choice == '3':
            patients = self.app.get_sorted_by_age(reverse=True)
            self.print_patient_table(patients, "Сортировка по возрасту (пожилые->молодые)")
        elif choice == '4':
            patients = self.app.get_sorted_by_cost()
            self.print_patient_table(patients, "Сортировка по стоимости лечения")
        else:
            print("\n   Неверный выбор")
    
    def filter_patients_flow(self) -> None:
        """Сценарий фильтрации."""
        self.print_header("ФИЛЬТРАЦИЯ")
        
        print("\n   1. Пожилые пациенты (>65 лет)")
        print("   2. Срочная помощь")
        print("   3. Стационарные пациенты")
        print("   4. Амбулаторные пациенты")
        
        choice = input("\n   Выберите фильтр: ").strip()
        
        if choice == '1':
            patients = self.app.filter_seniors()
            self.print_patient_table(patients, "Пожилые пациенты (>65 лет)")
        elif choice == '2':
            patients = self.app.filter_urgent()
            self.print_patient_table(patients, "Срочная помощь")
        elif choice == '3':
            patients = self.app.filter_inpatients()
            self.print_patient_table(patients, "Стационарные пациенты")
        elif choice == '4':
            patients = self.app.filter_outpatients()
            self.print_patient_table(patients, "Амбулаторные пациенты")
        else:
            print("\n   Неверный выбор")
    
    def show_statistics_flow(self) -> None:
        """Показать статистику."""
        self.print_header("СТАТИСТИКА")
        
        stats = self.app.get_statistics()
        
        print(f"\n      Всего пациентов: {stats['total']}")
        print(f"      Стационарных: {stats['inpatients']}")
        print(f"      Амбулаторных: {stats['outpatients']}")
        print(f"      Пожилых (>65): {stats['seniors']}")
        print(f"      Требуют срочной помощи: {stats['urgent']}")
        print(f"      Общая стоимость лечения: {stats['total_cost']} руб.")
    
    def main_menu(self) -> None:
        """Главное меню."""
        while True:
            print("\n" + "="*60)
            print("          МЕДИЦИНСКАЯ ИНФОРМАЦИОННАЯ СИСТЕМА")
            print("="*60)
            print("\n   1. Добавить обычного пациента")
            print("   2. Добавить стационарного пациента")
            print("   3. Добавить амбулаторного пациента")
            print("   4. Показать всех пациентов")
            print("   5. Найти пациента")
            print("   6. Удалить пациента")
            print("   7. Сортировка")
            print("   8. Фильтрация")
            print("   9. Статистика")
            print("   0. Выход")
            print("="*60)
            
            choice = input("\n   Выберите пункт меню: ").strip()
            
            if choice == '1':
                self.add_patient_flow()
            elif choice == '2':
                self.add_inpatient_flow()
            elif choice == '3':
                self.add_outpatient_flow()
            elif choice == '4':
                self.show_all_patients_flow()
            elif choice == '5':
                self.find_patient_flow()
            elif choice == '6':
                self.remove_patient_flow()
            elif choice == '7':
                self.sort_patients_flow()
            elif choice == '8':
                self.filter_patients_flow()
            elif choice == '9':
                self.show_statistics_flow()
            elif choice == '0':
                print("\n   До свидания!")
                break
            else:
                print("\n   Неверный пункт меню. Попробуйте снова.")