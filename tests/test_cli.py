from click.testing import CliRunner, Result
import pytest
from pytest_httpx import HTTPXMock

from jokes.app import jokes

from .factories import build_single_joke_response


class TestCLI:
    """Tests for the CLI commands."""

    @pytest.fixture(autouse=True)
    def set_common_fixtures(self, runner: CliRunner, httpx_mock: HTTPXMock):
        self.runner = runner
        self.mocker = httpx_mock

    def test_basic_cli_command(self):
        result = self.runner.invoke(jokes)

        assert result.exit_code == 0
        assert result.output is not None

    def test_non_existing_options(self):
        """Tests that invalid arguments throw an exception."""

        self.assert_exception(self.invoke_get(["-d", "nothing"]))

    def test_no_options(self):
        """Tests that the CLI works when no options are given."""

        self.mocker.add_response(json=build_single_joke_response().dict(exclude_none=True))
        self.assert_success(self.invoke_get())

    def test_all_options_together(self):
        """Tests all options together do not throw an exception."""

        self.mocker.add_response(json=build_single_joke_response().dict(exclude_none=True))
        self.assert_success(self.invoke_get(["-t", "TWOPART", "-c", "MISC", "-l", "FR", "-f" "NSFW", "--safe"]))

    @pytest.mark.parametrize(
        "arg, value, is_success",
        [
            ("-t", "single", True),
            ("--type", "single", True),
            ("-t", "twopart", True),
            ("--type", "twopart", True),
            ("-t", "random", False),
            ("--type", "nonexistent", False),
        ],
    )
    def test_type_options(self, arg: str, value: str, is_success: bool):
        """Tests valid and invalid type options."""

        self.assert_get_result([arg, value], is_success)

    @pytest.mark.parametrize(
        "arg, value, is_success",
        [
            ("-c", "any", True),
            ("--category", "any", True),
            ("-c", "misc", True),
            ("--category", "misc", True),
            ("-c", "programming", True),
            ("--category", "programming", True),
            ("-c", "dark", True),
            ("--category", "dark", True),
            ("-c", "pun", True),
            ("--category", "pun", True),
            ("-c", "spooky", True),
            ("--category", "spooky", True),
            ("-c", "christmas", True),
            ("--category", "christmas", True),
            ("-c", "random", False),
            ("--category", "nonexistent", False),
        ],
    )
    def test_category_options(self, arg: str, value: str, is_success: bool):
        """Tests valid and invalid category options."""

        self.assert_get_result([arg, value], is_success)

    @pytest.mark.parametrize(
        "arg, value, is_success",
        [
            ("-f", "nsfw", True),
            ("--flag", "nsfw", True),
            ("-f", "religious", True),
            ("--flag", "religious", True),
            ("-f", "political", True),
            ("--flag", "political", True),
            ("-f", "racist", True),
            ("--flag", "racist", True),
            ("-f", "sexist", True),
            ("--flag", "sexist", True),
            ("-f", "explicit", True),
            ("--flag", "explicit", True),
            ("-f", "random", False),
            ("--flag", "nonexistent", False),
        ],
    )
    def test_flag_options(self, arg: str, value: str, is_success: bool):
        """Tests valid and invalid flag options."""

        self.assert_get_result([arg, value], is_success)

    @pytest.mark.parametrize(
        "arg, value, is_success",
        [
            ("-l", "en", True),
            ("--lang", "en", True),
            ("-l", "fr", True),
            ("--lang", "fr", True),
            ("-l", "pt", True),
            ("--lang", "pt", True),
            ("-l", "es", True),
            ("--lang", "es", True),
            ("-l", "de", True),
            ("--lang", "de", True),
            ("-l", "cs", True),
            ("--lang", "cs", True),
            ("-l", "invalid", False),
            ("--lang", "invalid", False),
        ],
    )
    def test_language_options(self, arg: str, value: str, is_success: bool):
        """Tests valid and invalid language options."""

        self.assert_get_result([arg, value], is_success)

    def assert_get_result(self, args: list[str], is_success: bool):
        """
        Uses the parameters to get a result and calls a particul function
        based on whether the result is meant to be a success or throw an exception.
        """
        if is_success:
            self.mocker.add_response(json=build_single_joke_response().dict(exclude_none=True))

        assertion = self.assert_success if is_success else self.assert_exception

        return assertion(self.invoke_get(args))

    def invoke_get(self, args: list[str] = []) -> Result:
        """Invokes the get command with the given arguments and returns the result."""

        return self.runner.invoke(jokes, ["get", *args])

    def assert_success(self, result: Result) -> None:
        """Checks that the result did not throw an exception."""

        assert result.exception is None
        assert result.output is not None

    def assert_exception(self, result: Result) -> None:
        """Checks that the result threw an exception."""

        assert result.exception is not None
