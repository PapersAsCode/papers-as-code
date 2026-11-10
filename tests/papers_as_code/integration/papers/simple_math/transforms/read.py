import csv
from pathlib import Path

from papers_as_code.transforms import SourceTransform

from ..type import Numbers


class ReadNumbers(SourceTransform[Numbers]):
    """Read a CSV file with a `number` column."""

    def __init__(self, path: Path):
        self.path = path

    def produce(self) -> Numbers:
        with self.path.open(newline="") as file:
            numbers = [int(row["number"]) for row in csv.DictReader(file)]

        return Numbers(numbers)
