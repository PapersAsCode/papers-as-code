from papers_as_code.transforms import Transform

from ..type import Numbers


class Multiply(Transform[Numbers, Numbers]):
    """Multiply every number by `factor`."""

    def __init__(self, factor: int):
        self.factor = factor

    def transform(self, value: Numbers) -> Numbers:
        return Numbers([number * self.factor for number in value.repr])
