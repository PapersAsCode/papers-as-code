from abc import ABC


class Schema(ABC):
    """The meaning of a type."""
    name: str
    version: str
    description: str
