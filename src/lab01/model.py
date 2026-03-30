"""Модель пациента для медицинской системы"""

from validate import (
    validate_name,
    validate_age,
    validate_diagnosis,
    validate_medical_record,
    validate_status
)


class Patient:
    """
    Класс пациента медицинского учреждения
    
    Атрибуты класса:
        total_patients: общее количество созданных пациентов
        hospital_name: название больницы (общее для всех пациентов)
    """
    
    # Атрибуты класса (для оценки 4-5)
    total_patients = 0
    hospital_name = "Городская клиническая больница №1"
    
    def __init__(self, name: str, age: int, diagnosis: str, medical_record: str = ""):
        """
        Конструктор класса Patient с валидацией
        
        Args:
            name: ФИО пациента
            age: возраст пациента
            diagnosis: диагноз
            medical_record: записи в медицинской карте
        """
        # Валидация через вызовы функций из модуля validate
        self._name = validate_name(name)
        self._age = validate_age(age)
        self._diagnosis = validate_diagnosis(diagnosis)
        self._medical_record = validate_medical_record(medical_record)
        self._status = "active"  # Статус для логического состояния
        
        # Увеличиваем счетчик пациентов
        Patient.total_patients += 1
        self._patient_id = Patient.total_patients
    
    # === Свойства (property) для чтения ===
    
    @property
    def name(self) -> str:
        """Имя пациента (только для чтения)"""
        return self._name
    
    @property
    def age(self) -> int:
        """Возраст пациента (только для чтения)"""
        return self._age
    
    @property
    def diagnosis(self) -> str:
        """Диагноз пациента"""
        return self._diagnosis
    
    @diagnosis.setter
    def diagnosis(self, value: str) -> None:
        """
        Setter для диагноза с валидацией
        Для оценки 4-5: setter с валидацией
        """
        self._diagnosis = validate_diagnosis(value)
    
    @property
    def medical_record(self) -> str:
        """Медицинская карта пациента"""
        return self._medical_record
    
    @medical_record.setter
    def medical_record(self, value: str) -> None:
        """Setter для медицинской карты"""
        self._medical_record = validate_medical_record(value)
    
    @property
    def status(self) -> str:
        """Статус пациента (только для чтения)"""
        return self._status
    
    @property
    def patient_id(self) -> int:
        """Уникальный ID пациента (только для чтения)"""
        return self._patient_id
    
    # === Бизнес-методы ===
    
    def add_medical_record(self, entry: str) -> str:
        """
        Добавление записи в медицинскую карту (бизнес-метод 1)
        
        Args:
            entry: новая запись
            
        Returns:
            str: обновленная медицинская карта
            
        Raises:
            ValueError: если пациент выписан (логическое состояние)
        """
        if self._status == "discharged":
            raise ValueError("Нельзя добавить запись выписанному пациенту")
        
        new_entry = f"[{self._get_current_date()}] {entry}"
        if self._medical_record == "Нет записей":
            self._medical_record = new_entry
        else:
            self._medical_record = f"{self._medical_record}\n{new_entry}"
        return self._medical_record
    
    def discharge(self) -> str:
        """
        Выписка пациента (бизнес-метод 2 - изменение состояния)
        
        Returns:
            str: сообщение о выписке
            
        Raises:
            ValueError: если пациент уже выписан
        """
        if self._status == "discharged":
            raise ValueError(f"Пациент {self._name} уже выписан")
        
        if self._status == "critical":
            print(f"Внимание! Пациент {self._name} в критическом состоянии!")
        
        self._status = "discharged"
        return f"Пациент {self._name} выписан из больницы"
    
    def update_status(self, new_status: str) -> str:
        """
        Обновление статуса пациента (бизнес-метод 3)
        
        Args:
            new_status: новый статус (active, critical, recovering)
            
        Returns:
            str: сообщение об изменении статуса
            
        Raises:
            ValueError: если статус некорректен или пациент выписан
        """
        if self._status == "discharged":
            raise ValueError("Нельзя изменить статус выписанного пациента")
        
        valid_statuses = ["active", "critical", "recovering"]
        if new_status not in valid_statuses:
            raise ValueError(f"Статус должен быть одним из {valid_statuses}")
        
        old_status = self._status
        self._status = new_status
        
        # Логическое поведение в зависимости от состояния
        if new_status == "critical":
            self.add_medical_record("ПАЦИЕНТ ПЕРЕВЕДЕН В КРИТИЧЕСКОЕ СОСТОЯНИЕ! Требуется немедленная помощь!")
        elif new_status == "recovering":
            self.add_medical_record("Состояние пациента улучшается, идет на поправку")
        
        return f"Статус пациента изменен с '{old_status}' на '{new_status}'"
    
    def get_age_category(self) -> str:
        """
        Определение возрастной категории (бизнес-метод 4)
        
        Returns:
            str: возрастная категория
        """
        if self._age < 18:
            return "Ребенок"
        elif self._age < 60:
            return "Взрослый"
        else:
            return "Пожилой"
    
    def _get_current_date(self) -> str:
        """Вспомогательный метод для получения текущей даты"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # === Магические методы ===
    
    def __str__(self) -> str:
        """
        Строковое представление для пользователя
        Улучшенное форматирование (f-string)
        """
        status_emoji = {
            "active": "✅",
            "discharged": "📋",
            "critical": "⚠️",
            "recovering": "🔄"
        }.get(self._status, "❓")
        
        return (
            f"{'='*50}\n"
            f"👨‍⚕️ ПАЦИЕНТ #{self._patient_id}\n"
            f"{'='*50}\n"
            f"📝 ФИО: {self._name}\n"
            f"🎂 Возраст: {self._age} лет ({self.get_age_category()})\n"
            f"🩺 Диагноз: {self._diagnosis}\n"
            f"📊 Статус: {status_emoji} {self._status.upper()}\n"
            f"📋 Мед. карта:\n   {self._medical_record.replace(chr(10), chr(10)+'   ')}\n"
            f"{'='*50}"
        )
    
    def __repr__(self) -> str:
        """
         Техническое представление для разработчиков
         """
        return f"Patient(name='{self._name}', age={self._age}, diagnosis='{self._diagnosis}')"
    
    def __eq__(self, other) -> bool:
        """
        Сравнение пациентов по имени, возрасту и диагнозу
        """
        if not isinstance(other, Patient):
            return False
        return (self._name == other._name and 
                self._age == other._age and 
                self._diagnosis == other._diagnosis)
    
    def __hash__(self) -> int:
        """Хеш для использования в множествах"""
        return hash((self._name, self._age, self._diagnosis))