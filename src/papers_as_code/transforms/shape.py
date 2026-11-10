"""
The shape of what a transform takes or gives: one value, or a tuple of several.
"""
import inspect
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, TypeVar, get_args, get_origin, get_type_hints


@dataclass(frozen=True)
class Shape:
    """One value (`many=False`), or a tuple of `count` values (`many=True`)."""

    many: bool
    count: int

    @classmethod
    def one(cls) -> "Shape":
        return cls(many=False, count=1)

    @classmethod
    def from_hint(cls, hint: Any) -> "Shape | None":
        """Return the shape a type hint describes, or None if it doesn't say."""
        if hint is None or hint is Any or hint is tuple or isinstance(hint, TypeVar):
            return None
        if get_origin(hint) is not tuple:
            return cls.one()

        args = get_args(hint)
        if Ellipsis in args:
            return None
        return cls(many=True, count=len(args))

    @classmethod
    def combine(cls, shapes: list["Shape"]) -> "Shape":
        """Return several shapes side by side, as one shape."""
        if len(shapes) == 1:
            return shapes[0]
        return cls(many=True, count=sum(shape.count for shape in shapes))

    def pack(self, values: tuple[Any, ...]) -> Any:
        """Turn one value per slot into the value a transform takes."""
        return values if self.many else values[0]

    def unpack(self, value: Any) -> tuple[Any, ...]:
        """Turn the value a transform takes into one value per slot."""
        return tuple(value) if self.many else (value,)


def annotated_shapes(method: Callable[..., Any]) -> tuple[Shape | None, Shape | None]:
    """Return the input and output shapes a method is annotated with."""
    try:
        hints = get_type_hints(method)
    except NameError:
        return None, None

    parameters = list(inspect.signature(method).parameters)
    input_hint = hints.get(parameters[0]) if parameters else None

    return Shape.from_hint(input_hint), Shape.from_hint(hints.get("return"))
