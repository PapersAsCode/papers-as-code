from typing import Any
from papers_as_code.type import Schema


class Type:
    schema: Schema

    def __init__(self, repr: Any, schema: Schema):
        self.schema = schema