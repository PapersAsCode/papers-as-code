from papers_as_code.transforms import Transform

from ..type import Numbers


class Add(Transform[Numbers, Numbers]):
    """Add `amount` to every number."""

    def __init__(self, amount: int):
        self.amount = amount

    def transform(self, value: Numbers) -> Numbers:
        return Numbers([number + self.amount for number in value.repr])
