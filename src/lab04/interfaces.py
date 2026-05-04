"""
Абстрактные базовые классы (интерфейсы) для ЛР-4
Предметная область: Медицина
"""

from abc import ABC, abstractmethod
from typing import Any


class Printable(ABC):
    @abstractmethod
    def get_short_info(self) -> str:
        pass


class Comparable(ABC):
    @abstractmethod
    def compare(self, other: Any) -> int:
        pass
    
    def __lt__(self, other):
        return self.compare(other) < 0
    
    def __le__(self, other):
        return self.compare(other) <= 0
    
    def __gt__(self, other):
        return self.compare(other) > 0
    
    def __ge__(self, other):
        return self.compare(other) >= 0
    
    def __eq__(self, other):
        return self.compare(other) == 0
    
    def __ne__(self, other):
        return self.compare(other) != 0