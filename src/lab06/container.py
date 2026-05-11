"""
Generic-коллекция и протоколы для ЛР-6
Предметная область: Медицина
"""

from typing import TypeVar, Generic, Callable, Optional, List, Protocol
from datetime import datetime


# ============================================================================
# TypeVar для Generic-коллекции (оценка 3)
# ============================================================================

T = TypeVar('T')           # Тип элементов коллекции (любой)
R = TypeVar('R')           # Тип результата преобразования (для map)


# ============================================================================
# Протоколы (оценка 5)
# ============================================================================

class Displayable(Protocol):
    """
    Протокол для объектов, которые можно отобразить.
    Достаточно наличия метода display() -> str.
    """
    def display(self) -> str:
        ...


class Scorable(Protocol):
    """
    Протокол для объектов, которые имеют оценку/приоритет.
    Достаточно наличия метода get_score() -> float.
    """
    def get_score(self) -> float:
        ...


# ============================================================================
# TypeVar с ограничениями (bound) для протоколов (оценка 5)
# ============================================================================

D = TypeVar('D', bound=Displayable)   # Только объекты с методом display()
S = TypeVar('S', bound=Scorable)      # Только объекты с методом get_score()


# ============================================================================
# GENERIC-КОЛЛЕКЦИЯ TYPEDCOLLECTION (оценка 3, 4, 5)
# ============================================================================

class TypedCollection(Generic[T]):
    """
    Типизированная коллекция.
    Может хранить объекты только одного типа T.
    Поддерживает добавление, удаление, поиск, фильтрацию, отображение.
    """
    
    def __init__(self) -> None:
        """Инициализация пустой коллекции."""
        self._items: List[T] = []
    
    # ========== Базовые операции (из ЛР-2) ==========
    
    def add(self, item: T) -> None:
        """
        Добавить элемент в коллекцию.
        
        Args:
            item: Элемент типа T
        """
        self._items.append(item)
        print(f"      + Добавлен: {item}")
    
    def remove(self, item: T) -> bool:
        """
        Удалить элемент из коллекции.
        
        Args:
            item: Элемент для удаления
            
        Returns:
            True если удалён, False если не найден
        """
        if item in self._items:
            self._items.remove(item)
            print(f"      - Удалён: {item}")
            return True
        print(f"      Ошибка: элемент не найден")
        return False
    
    def remove_at(self, index: int) -> Optional[T]:
        """
        Удалить элемент по индексу.
        
        Args:
            index: Индекс для удаления
            
        Returns:
            Удалённый элемент или None
        """
        if 0 <= index < len(self._items):
            removed: T = self._items.pop(index)
            print(f"      - Удалён по индексу {index}: {removed}")
            return removed
        print(f"      Ошибка: индекс {index} вне диапазона")
        return None
    
    def get_all(self) -> List[T]:
        """
        Получить копию списка всех элементов.
        
        Returns:
            Копия внутреннего списка
        """
        return self._items.copy()
    
    def __len__(self) -> int:
        """Вернуть количество элементов."""
        return len(self._items)
    
    def __iter__(self):
        """Вернуть итератор для перебора."""
        return iter(self._items)
    
    def __getitem__(self, index: int) -> T:
        """
        Доступ по индексу.
        
        Args:
            index: Индекс (поддерживает отрицательные)
            
        Returns:
            Элемент по индексу
        """
        if isinstance(index, int):
            if index < 0:
                index = len(self._items) + index
            if 0 <= index < len(self._items):
                return self._items[index]
            raise IndexError(f"Индекс {index} вне диапазона")
        raise TypeError("Индекс должен быть целым числом")
    
    def print_all(self, title: str = "Коллекция") -> None:
        """Вывести все элементы."""
        if not self._items:
            print("      Коллекция пуста")
            return
        print(f"\n      {title} ({len(self._items)}):")
        print("      " + "-"*40)
        for i, item in enumerate(self._items):
            print(f"      [{i}] {item}")
        print()
    
    # ========== Новые методы (оценка 4) ==========
    
    def find(self, predicate: Callable[[T], bool]) -> Optional[T]:
        """
        Найти первый элемент, удовлетворяющий условию.
        
        Args:
            predicate: Функция-условие (принимает T, возвращает bool)
            
        Returns:
            Первый подходящий элемент или None
        """
        for item in self._items:
            if predicate(item):
                print(f"      Найден: {item}")
                return item
        print(f"      Не найден")
        return None
    
    def filter(self, predicate: Callable[[T], bool]) -> List[T]:
        """
        Отфильтровать элементы по условию.
        
        Args:
            predicate: Функция-условие (принимает T, возвращает bool)
            
        Returns:
            Список подходящих элементов
        """
        result: List[T] = [item for item in self._items if predicate(item)]
        print(f"      Отфильтровано {len(result)} элементов")
        return result
    
    def map(self, transform: Callable[[T], R]) -> List[R]:
        """
        Применить функцию преобразования к каждому элементу.
        
        Args:
            transform: Функция преобразования (T -> R)
            
        Returns:
            Список результатов преобразования
        """
        result: List[R] = [transform(item) for item in self._items]
        print(f"      Преобразовано {len(result)} элементов")
        return result


# ============================================================================
# TYPEDCOLLECTION С ОГРАНИЧЕНИЯМИ (ДЛЯ СЦЕНАРИЯ 5)
# ============================================================================

class TypedDisplayCollection(Generic[D]):
    """
    Типизированная коллекция для объектов с методом display().
    Использует TypeVar с bound=Displayable.
    """
    
    def __init__(self) -> None:
        self._items: List[D] = []
    
    def add(self, item: D) -> None:
        self._items.append(item)
        print(f"      + Добавлен: {item.display()}")
    
    def get_all(self) -> List[D]:
        return self._items.copy()
    
    def display_all(self) -> None:
        """Вывести все элементы через метод display()."""
        print("\n      Displayable коллекция:")
        for i, item in enumerate(self._items):
            print(f"      [{i}] {item.display()}")
    
    def __len__(self) -> int:
        return len(self._items)


class TypedScoreCollection(Generic[S]):
    """
    Типизированная коллекция для объектов с методом get_score().
    Использует TypeVar с bound=Scorable.
    """
    
    def __init__(self) -> None:
        self._items: List[S] = []
    
    def add(self, item: S) -> None:
        self._items.append(item)
        print(f"      + Добавлен: {item.display() if hasattr(item, 'display') else str(item)}")
    
    def get_all(self) -> List[S]:
        return self._items.copy()
    
    def get_sorted_by_score(self) -> List[S]:
        """Вернуть элементы, отсортированные по score()."""
        return sorted(self._items, key=lambda x: x.get_score(), reverse=True)
    
    def print_scores(self) -> None:
        """Вывести все элементы с их оценками."""
        print("\n      Score коллекция:")
        for i, item in enumerate(self._items):
            display_str = item.display() if hasattr(item, 'display') else str(item)
            print(f"      [{i}] {display_str} | Score: {item.get_score()}")
    
    def __len__(self) -> int:
        return len(self._items)