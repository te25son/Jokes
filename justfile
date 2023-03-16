default: fix

locations := "./src ./tests"

alias t := test
alias f := fix
alias c := check

# Show all available recipes
help:
    @just -l

# Run all tests
test:
    pytest -n 2 --cov --random-order

# Run linter and formatter
fix: (lint) (format) (pre-commit-fix)

# Run lint, format, and type checks
check: (lint-check) (format-check) (type-check) (pre-commit-check)

_lint args="":
    ruff {{locations}} {{args}}

# Run linter
lint: (_lint)

# Run linter and throw error on fix
lint-check: (_lint "--exit-non-zero-on-fix")

_format args="":
    black {{locations}} {{args}}

# Run formatter
format: (_format)

# Run formatter and throw error on fix
format-check: (_format "--check")

# Run type checker
type-check:
    mypy {{locations}}

_pre-commit +hooks:
    @for hook in {{hooks}}; do \
        pre-commit run $hook --all-files; \
    done;

# Run misc pre commit checks
pre-commit-check: (_pre-commit "check-toml" "check-yaml" "check-json")

# Runs misc pre commit fixes
pre-commit-fix: (_pre-commit "end-of-file-fixer" "trailing-whitespace")
