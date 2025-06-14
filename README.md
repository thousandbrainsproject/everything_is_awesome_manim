# everything_is_awesome_manim

Manim animation for https://github.com/thousandbrainsproject/everything_is_awesome May 2025 Hackathon project.

## Development

The development of this project is managed with [uv](https://docs.astral.sh/uv/), "a single tool to replace `pip`, `pip-tools`, `pipx`, `poetry`, `pyenv`, `twine`, `virtualenv`, and more." You will need to install it.

We use `uv` as it tracks the latest PEP standards while relying on existing infrastructure like `pip`, `venv`, etc.

`uv.lock` is non-standard in Python, but as Python does not yet define a lockfile standard, any lockfile format is non-standard. The benefit of `uv.lock` is that it is cross-platform and "captures the packages that would be installed across all possible Python markers such as operating system, architecture, and Python version". This makes it safe to check-in to the repository.

### Install `uv`

On a Mac, `brew install uv` is sufficient. For additional options, see the [uv installation instructions](https://docs.astral.sh/uv/getting-started/installation/).

### Install dependencies

```bash
uv sync
```

### Run formatter

```bash
uv run ruff format
```

### Run style checks

```bash
uv run ruff check
```

### Run dependency checks

```bash
uv run deptry src tests
```

### Run static type checks

```bash
uv run mypy
```

### Run tests

```bash
uv run pytest
```

### Build package

```bash
uv build
```
