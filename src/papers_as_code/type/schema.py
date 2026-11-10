from abc import ABC, abstractmethod


class Schema(ABC):
    """The format for a type"""

    @abstractmethod
    def validate(self) -> bool:
        return True