from papers_as_code.type.schema import Schema
from papers_as_code.type.type import Type


class NullSchema(Schema):
    name = "null"
    version = "0.1.0"
    description = "No data"


class Null(Type[None]):
    """No data: what a source takes as input, and a sink gives as output."""

    schema = NullSchema()

    def __init__(self) -> None:
        super().__init__(None)
