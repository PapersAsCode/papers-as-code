# papers-as-code
Reproducible, shareable scientific papers.

Infrastructure as code, but for scientific papers. A paper is defined in code, and everything in it (data, figures, tables, transforms, numbers in the text) is an artifact that can be traced back to, and regenerated from, the code that produced it, sent and fetched to and from online registries.

## Development
Checks are run with [tox](https://tox.wiki):

```sh
tox                 # run everything
tox -e py313        # unit tests
tox -e lint         # flake8
tox -e format       # black, isort, autoflake
tox -e typecheck    # mypy
tox -e docstrings   # pydocstyle (numpy convention)
```
