import logging

_ROOT_NAME = "papers_as_code"
_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"


def get_logger(name: str) -> logging.Logger:
    """Return the logger for `name`, typically `__name__`."""
    root = logging.getLogger(_ROOT_NAME)
    if not root.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(_FORMAT))
        root.addHandler(handler)
        root.setLevel(logging.INFO)

    return root.getChild(name.removeprefix(f"{_ROOT_NAME}."))
