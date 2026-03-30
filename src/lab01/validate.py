"""Модуль валидации для класса Patient"""

def validate_name(name: str, field_name: str = "Имя") -> str:
    """
    Проверка имени пациента
    
    Args:
        name: проверяемое имя
        field_name: название поля для сообщения об ошибке
        
    Returns:
        str: проверенное имя
        
    Raises:
        ValueError: если имя некорректно
    """
    if not isinstance(name, str):
        raise ValueError(f"{field_name} должно быть строкой, получено {type(name).__name__}")
    
    if not name.strip():
        raise ValueError(f"{field_name} не может быть пустым")
    
    if len(name.strip()) < 2:
        raise ValueError(f"{field_name} должно содержать минимум 2 символа")
    
    return name.strip()


def validate_age(age: int) -> int:
    """
    Проверка возраста пациента
    
    Args:
        age: проверяемый возраст
        
    Returns:
        int: проверенный возраст
        
    Raises:
        ValueError: если возраст некорректен
    """
    if not isinstance(age, int):
        raise ValueError(f"Возраст должен быть целым числом, получено {type(age).__name__}")
    
    if age < 0:
        raise ValueError(f"Возраст не может быть отрицательным: {age}")
    
    if age > 150:
        raise ValueError(f"Возраст не может превышать 150 лет: {age}")
    
    return age


def validate_diagnosis(diagnosis: str) -> str:
    """
    Проверка диагноза пациента
    
    Args:
        diagnosis: проверяемый диагноз
        
    Returns:
        str: проверенный диагноз
        
    Raises:
        ValueError: если диагноз некорректен
    """
    if not isinstance(diagnosis, str):
        raise ValueError(f"Диагноз должен быть строкой, получено {type(diagnosis).__name__}")
    
    if not diagnosis.strip():
        raise ValueError("Диагноз не может быть пустым")
    
    return diagnosis.strip()


def validate_medical_record(medical_record: str) -> str:
    """
    Проверка медицинской карты
    
    Args:
        medical_record: проверяемая медицинская карта
        
    Returns:
        str: проверенная медицинская карта
        
    Raises:
        Value
        Error: если медицинская карта некорректна
    """
    if not isinstance(medical_record, str):
        raise ValueError(f"Медицинская карта должна быть строкой, получено {type(medical_record).__name__}")
    
    # Медицинская карта может быть пустой (новая запись)
    return medical_record.strip() if medical_record else "Нет записей"


def validate_status(status: str) -> str:
    """
    Проверка статуса пациента
    
    Args:
        status: проверяемый статус
        
    Returns:
        str: проверенный статус
        
    Raises:
        ValueError: если статус некорректен
    """
    valid_statuses = ["active", "discharged", "critical", "recovering"]
    
    if not isinstance(status, str):
        raise ValueError(f"Статус должен быть строкой, получено {type(status).__name__}")
    
    if status not in valid_statuses:
        raise ValueError(f"Статус должен быть одним из {valid_statuses}, получено '{status}'")
    
    return status