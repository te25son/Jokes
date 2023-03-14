import nox
from nox.sessions import Session

python_versions = ["3.10"]
locations = ("src", "tests", "noxfile.py")


@nox.session(python=python_versions)
def tests(session: Session) -> None:
    args = session.posargs or ["--cov"]
    # Poetry is not a part of the environment created by Nox, so we specify external
    # to avoid warnings about external commands leaking into the isolated test environments.
    session.run("poetry", "install", external=True)
    session.run("pytest", *args)


@nox.session(python=python_versions)
def lint(session: Session) -> None:
    args = session.posargs or locations
    session.install("ruff")
    session.run("ruff", *args)


@nox.session(python=python_versions[0], tags=["clean"])
def black(session: Session) -> None:
    args = session.posargs or locations
    session.install("black")
    session.run("black", *args)
