"""
Собственные исключения для предметной области
"""


class PatientNotFoundError(Exception):
    """Пациент не найден в коллекции."""
    pass


class DuplicatePatientError(Exception):
    """Пациент с таким ID уже существует."""
    pass


class InvalidAgeError(Exception):
    """Некорректный возраст пациента."""
    pass


class InvalidInputError(Exception):
    """Некорректный ввод пользователя."""
    pass