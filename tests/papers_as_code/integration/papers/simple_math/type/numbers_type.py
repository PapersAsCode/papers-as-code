from papers_as_code.type import Type

from .schema import NumbersSchema


class Numbers(Type[list[int]]):
    """A list of numbers."""

    schema = NumbersSchema()
