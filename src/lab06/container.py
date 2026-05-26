"""
Generic-коллекция и протоколы для ЛР-6
"""

from typing import TypeVar, Generic, Callable, Optional, List, Protocol


class Displayable(Protocol):
    def display(self) -> str:
        ...


class Scorable(Protocol):
    def get_score(self) -> float:
        ...


T = TypeVar('T')
R = TypeVar('R')
D = TypeVar('D', bound=Displayable)
S = TypeVar('S', bound=Scorable)


class TypedCollection(Generic[T]):
    
    def __init__(self) -> None:
        self._items: List[T] = []
    
    def add(self, item: T) -> None:
        self._items.append(item)
        print(f"      + Добавлен: {item}")
    
    def remove(self, item: T) -> bool:
        if item in self._items:
            self._items.remove(item)
            print(f"      - Удалён: {item}")
            return True
        print(f"      Ошибка: элемент не найден")
        return False
    
    def remove_at(self, index: int) -> Optional[T]:
        if 0 <= index < len(self._items):
            removed = self._items.pop(index)
            print(f"      - Удалён по индексу {index}: {removed}")
            return removed
        print(f"      Ошибка: индекс {index} вне диапазона")
        return None
    
    def get_all(self) -> List[T]:
        return self._items.copy()
    
    def __len__(self) -> int:
        return len(self._items)
    
    def __iter__(self):
        return iter(self._items)
    
    def __getitem__(self, index: int) -> T:
        if isinstance(index, int):
            if index < 0:
                index = len(self._items) + index
            if 0 <= index < len(self._items):
                return self._items[index]
            raise IndexError(f"Индекс {index} вне диапазона")
        raise TypeError("Индекс должен быть целым числом")
    
    def print_all(self, title: str = "Коллекция") -> None:
        if not self._items:
            print("      Коллекция пуста")
            return
        print(f"\n      {title} ({len(self._items)}):")
        print("      " + "-"*40)
        for i, item in enumerate(self._items):
            print(f"      [{i}] {item}")
        print()
    
    def find(self, predicate: Callable[[T], bool]) -> Optional[T]:
        for item in self._items:
            if predicate(item):
                print(f"      Найден: {item}")
                return item
        print(f"      Не найден")
        return None
    
    def filter(self, predicate: Callable[[T], bool]) -> List[T]:
        result = [item for item in self._items if predicate(item)]
        print(f"      Отфильтровано {len(result)} элементов")
        return result
    
    def map(self, transform: Callable[[T], R]) -> List[R]:
        result = [transform(item) for item in self._items]
        print(f"      Преобразовано {len(result)} элементов")
        return result
    
    def display_all(self) -> None:
        print("\n      Displayable коллекция:")
        for i, item in enumerate(self._items):
            if hasattr(item, 'display'):
                print(f"      [{i}] {item.display()}")
            else:
                print(f"      [{i}] {item}")
    
    def print_scores(self) -> None:
        print("\n      Score коллекция:")
        for i, item in enumerate(self._items):
            score = item.get_score() if hasattr(item, 'get_score') else 0
            display_str = item.display() if hasattr(item, 'display') else str(item)
            print(f"      [{i}] {display_str} | Score: {score}")
    
    def get_sorted_by_score(self) -> List[T]:
        return sorted(self._items, key=lambda x: x.get_score() if hasattr(x, 'get_score') else 0, reverse=True)