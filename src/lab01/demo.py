"""Демонстрационный файл для класса Patient"""

from model import Patient


def main():
    print("\n" + "="*60)
    print("🏥 ДЕМОНСТРАЦИЯ РАБОТЫ КЛАССА PATIENT")
    print("="*60)
    
    # ========== ДЕМОНСТРАЦИЯ ДЛЯ ОЦЕНКИ 3 ==========
    print("\n📌 ЧАСТЬ 1: БАЗОВАЯ ДЕМОНСТРАЦИЯ (оценка 3)")
    print("-" * 50)
    
    # Создание объекта
    patient1 = Patient("Иванов Иван Иванович", 35, "Гипертония", "Первичный осмотр")
    
    # Вывод через print (использует __str__)
    print(patient1)
    
    # Сравнение двух объектов (__eq__)
    patient2 = Patient("Петрова Анна Сергеевна", 28, "Грипп", "Температура 38.5")
    patient3 = Patient("Иванов Иван Иванович", 35, "Гипертония", "Первичный осмотр")
    
    print("\n🔍 Сравнение пациентов:")
    print(f"patient1 == patient2: {patient1 == patient2}")
    print(f"patient1 == patient3: {patient1 == patient3}")
    
    # Пример некорректного создания (try/except)
    print("\n❌ Попытка создать пациента с некорректными данными:")
    try:
        invalid_patient = Patient("", -5, "Простуда")
    except ValueError as e:
        print(f"   Ошибка: {e}")
    
    # ========== ДЕМОНСТРАЦИЯ ДЛЯ ОЦЕНКИ 4 ==========
    print("\n\n📌 ЧАСТЬ 2: РАСШИРЕННАЯ ДЕМОНСТРАЦИЯ (оценка 4)")
    print("-" * 50)
    
    # Демонстрация __repr__
    print(f"\n🔧 Техническое представление (__repr__):")
    print(f"   {repr(patient1)}")
    
    # Демонстрация setter с валидацией
    print(f"\n🩺 Текущий диагноз {patient1.name}: {patient1.diagnosis}")
    try:
        patient1.diagnosis = "Артериальная гипертензия 2 степени"
        print(f"   ✅ Диагноз изменен на: {patient1.diagnosis}")
        
        # Попытка установить некорректный диагноз
        patient1.diagnosis = ""
    except ValueError as e:
        print(f"   ❌ Ошибка при смене диагноза: {e}")
    
    # Атрибут класса
    print(f"\n🏥 Атрибут класса - больница: {Patient.hospital_name}")
    print(f"   Доступ через экземпляр: {patient1.hospital_name}")
    print(f"   Всего создано пациентов: {Patient.total_patients}")
    
    # Второй бизнес-метод
    print(f"\n📊 Возрастная категория {patient1.name}: {patient1.get_age_category()}")
    
    # ========== ДЕМОНСТРАЦИЯ ДЛЯ ОЦЕНКИ 5 ==========
    print("\n\n📌 ЧАСТЬ 3: РАСШИРЕННАЯ ДЕМОНСТРАЦИЯ (оценка 5)")
    print("-" * 50)
    
    # Создание нового пациента
    patient4 = Patient("Сидоров Петр Васильевич", 72, "Пневмония", "Поступил с кашлем")
    print(patient4)
    
    # Сценарий 1: Изменение состояния пациента
    print("\n🎬 СЦЕНАРИЙ 1: Изменение статуса пациента")
    print(f"   Текущий статус: {patient4.status}")
    
    # Обновление статуса
    result = patient4.update_status("critical")
    print(f"   {result}")
    print(f"   Новый статус: {patient4.status}")
    
    # Попытка добавить запись в критическом состоянии
    print("\n📝 Добавление записи в медкарту:")
    patient4.add_medical_record("Назначено срочное КТ")
    print(f"   Запись добавлена")
    
    # Сценарий 2: Выписка пациента
    print("\n🎬 СЦЕНАРИЙ 2: Выписка пациента")
    result = patient4.discharge()
    print(f"   {result}")
    print(f"   Статус после выписки: {patient4.status}")
    
    # Попытка изменить статус выписанного пациента (логическое состояние)
    print("\n❌ Попытка изменить статус выписанного пациента:")
    try:
        patient4.update_status("recovering")
    except ValueError as e:
        print(f"   Ошибка: {e}")
    
    # Сценарий 3: Демонстрация всех валидаций
    print("\n🎬 СЦЕНАРИЙ 3: Валидация данных")
    
    # Создание пациента с нормальными данными
    try:
        patient5 = Patient("Тестов Тест Тестович", 25, "Здоров", "")
        print(f"   ✅ Пациент успешно создан: {patient5.name}")
    except ValueError as e:
        print(f"   Ошибка: {e}")
    
    # Проверка возраста
    print("\n🔍 Проверка возраста:")
    try:
        invalid_age = Patient("Неверный", -10, "Простуда")
    except ValueError as e:
        print(f"   ❌ {e}")
    
    try:
        invalid_age2 = Patient("Неверный", 200, "Простуда")
    except ValueError as e:
        print(f"   ❌ {e}")
    
    # Проверка имени
    print("\n🔍 Проверка имени:")
    try:
        invalid_name = Patient("", 30, "Простуда")
    except ValueError as e:
        print(f"   ❌ {e}")
    
    try:
        invalid_name2 = Patient("A", 30, "Простуда")
    except ValueError as e:
        print(f"   ❌ {e}")
    
    # Проверка типа данных
    print("\n🔍 Проверка типа данных:")
    try:
        invalid_type = Patient(123, 30, "Простуда")
    except ValueError as e:
        print(f"   ❌ {e}")
    
    # Демонстрация статистики
    print("\n📊 ИТОГОВАЯ СТАТИСТИКА:")
    print(f"   Всего создано пациентов: {Patient.total_patients}")
    print(f"   Название больницы: {Patient.hospital_name}")
    
    # Сравнение хешей (для множеств)
    print("\n🔢 Работа с множеством пациентов:")
    patients_set = {patient1, patient2, patient3}
    print(f"   Уникальных пациентов в множестве: {len(patients_set)}")
    print(f"   (patient1 и patient3 одинаковы, поэтому в множестве только 2)")
    
    print("\n" + "="*60)
    print("🏁 ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()