# pyproject.toml Template

Reference template for uv-native Python projects.

```toml
[project]
name = "{PROJECT_NAME}"
version = "0.1.0"
description = "{DESCRIPTION}"
requires-python = ">=3.11"
dependencies = [
    # Add production dependencies here
]

[dependency-groups]
dev = [
    "pytest>=8.0",
    "pytest-asyncio>=0.24",
    "pytest-cov>=5.0",
    "mypy>=1.11",
    "ruff>=0.8",
    "pre-commit>=4.0",
]

[tool.ruff]
line-length = 120
target-version = "py311"

[tool.ruff.lint]
select = ["F", "E", "W", "I", "N", "D", "UP", "S", "B", "C4", "PT", "RUF"]
ignore = ["D100", "D101", "D102", "D103", "D104", "D105", "D107"]

[tool.ruff.lint.pydocstyle]
convention = "google"

[tool.ruff.format]
quote-style = "double"
indent-style = "space"

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
addopts = ["-v", "--strict-markers"]

[tool.mypy]
python_version = "3.11"
warn_return_any = true
ignore_missing_imports = true

[tool.coverage.run]
source = ["."]
omit = ["*/tests/*", ".venv/*"]
```

## Placeholders

| Placeholder | Description |
|-------------|-------------|
| {PROJECT_NAME} | Project name from directory or pyproject.toml |
| {DESCRIPTION} | Short project description |
