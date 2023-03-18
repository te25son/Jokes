_default:
    just fix "--all"
    just check "--all"

locations := "./src ./tests"

[private]
alias t := test
[private]
alias f := fix
[private]
alias c := check
[private]
alias h := help
[private]
alias p := pre-commit-all

# Show all available recipes
help:
    @just --list --list-prefix "···· "

# Set up the project locally
setup:
    poetry install
    pre-commit install
    @echo "\nSetup finished. Conisider running 'poetry shell' to activate the virtual environment."

# Run all tests
test:
    pytest -n 2 --cov --random-order

# Run linter and formatter (only run pre-commit if flag is "--all" or "-a")
fix *flags: (lint) (format)
    @if [[ '{{ flags }}' == '--all' || '{{ flags }}' == '-a' ]]; then \
        just _pre-commit "end-of-file-fixer" "trailing-whitespace"; \
    fi

# Run lint, format, and type checks (only run pre-commit if flag is "--all" or "-a")
check *flags: (lint "--exit-non-zero-on-fix") (format "--check") (type-check)
    @if [[ '{{ flags }}' == '--all' || '{{ flags }}' == '-a' ]]; then \
        just _pre-commit "check-toml" "check-yaml" "check-json"; \
    fi

# Run linter on locations with optional arguments
lint *args:
    ruff {{ locations }} {{ args }}

# Run formatter on locations with optional arguments
format *args:
    black {{ locations }} {{ args }}

# Run type checker on locations with optional arguments
type-check *args:
    mypy {{ locations }} {{ args }}

_pre-commit +hooks:
    @for hook in {{ hooks }}; do \
        pre-commit run $hook --all-files; \
    done;

# Run all pre-commit hooks on all files
pre-commit-all:
    pre-commit run --all-files
