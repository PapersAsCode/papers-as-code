from pathlib import Path

from papers_as_code.type import Null

from ..transforms import Add, Multiply, ReadNumbers

NUMBERS_CSV = Path(__file__).parent.parent / "data" / "numbers.csv"


def test_read_numbers() -> None:
    numbers = ReadNumbers(NUMBERS_CSV).produce()

    assert numbers.repr == [1, 2, 3]


def test_multiply() -> None:
    pipeline = ReadNumbers(NUMBERS_CSV) >> Multiply(10)

    assert pipeline.transform(Null()).repr == [10, 20, 30]


def test_multiply_then_add() -> None:
    pipeline = ReadNumbers(NUMBERS_CSV) >> Multiply(10) >> Add(1)

    assert pipeline.transform(Null()).repr == [11, 21, 31]
