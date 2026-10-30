# Contributing to papers-as-code
For those interested in developing for papers-as-code, below I share ways to get started and some of the conventions we use.

## Development
We use poetry for package and dependency management. You can install poetry system-wide with pipx:

```bash
pipx install poetry
```

To lock and install dependencies run

```bash
poetry lock
poetry install
```

To enter the Python virtual environment run

```bash
eval $(poetry env activate)
```

If a suitable Python version cannot be found, it's recommended to use `pyenv` to install it, e.g., `pyenv install 3.13.0`.

Note this doesn't spawn a subshell, so `exit` will close your shell entirely. It is important to enter the virtual environment before installing dependencies.

To build the project just run

```bash
poetry build
```

And the source and binary distributions will appear in the `dist/` folder.

## Working with papers-as-code source maps
Projects that depend on papers-as-code can link not to the PyPI-installed version, but to a local copy, for instance for debugging purposes.

Within the environment of your project, use the `--editable` option to install papers-as-code with the source maps

```bash
pip install -e [path]
```

Then your dependency updates with the changes made locally, and even the debugger and IntelliSense will take note of this.

## Testing
Run pytest as usual. In the root of the project run
```bash
pytest
```

And tox tests in python 3.13 can be run with, say
```bash
tox -e py313 -- --randomly-seed=1234
```
The seed is optional, and will shuffle the order of the tests and is good practice.
To run the full suite with linting, formatting, type-checking and docstring checks, install tox (e.g. with `pipx install tox`) and run `tox`.

## Lint and Typecheck Locally
Install `black`, `isort`, `autoflake`, `flake8`, `mypy`, `pydocstyle` system-wide with `pipx` or in your environment with `pip`. Go to the repository root and run `black .`, `isort .`, `autoflake .`, `flake8 src tests`, `mypy src tests` and `pydocstyle src` to lint/format/type-check.

It is recommended to run the corresponding tox environments for these commands (`tox -e lint`, `tox -e format`, `tox -e typecheck`, `tox -e docstrings`); these are exactly what CI runs, and `tox.ini` already takes any extra dependencies into account.

Docstrings follow the [numpy convention](https://numpydoc.readthedocs.io/en/latest/format.html).

## Commits and Semantic Versioning
We bump our releases and update our changelog automatically, but this requires commits to follow the [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/) scheme. We use a combination of [release-please](https://github.com/googleapis/release-please) and [commitlint](https://commitlint.js.org/).

We recommend using squash-merge for pull requests for many reasons. Rebase-merge works too, but if you're doing something like red/green development and did not validate all your individual commits against the actions, the main branch may not be clean after a rebase-merge (in the sense that every commit be "green").

```note
Note: if squashing or rebasing, the commit message must conform to commitlint's rules, otherwise release-please will not create a PR
```
