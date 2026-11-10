from papers_as_code.type.schema import Schema
from papers_as_code.type.type import Type


class NullSchema(Schema):
    """The format of a value that holds no data."""

    def validate(self) -> bool:
        return True


class Null(Type):
    """No data: what a source takes as input, and a sink gives as output."""

    def __init__(self) -> None:
        super().__init__(None, NullSchema())
