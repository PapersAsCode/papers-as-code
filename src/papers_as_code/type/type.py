from abc import ABC
from typing import ClassVar

from papers_as_code.type.schema import Schema


class Type[R](ABC):
    """A value, held as its representation `repr`, with a schema giving it meaning."""

    schema: ClassVar[Schema]
    repr: R

    def __init__(self, repr: R):
        self.repr = repr

    def validate(self) -> bool:
        raise NotImplementedError
