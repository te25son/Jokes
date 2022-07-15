import pytest

from click.testing import CliRunner, Result
from jokes.app import main


class TestCLI:
    @pytest.fixture(autouse=True)
    def set_common_fixtures(self, runner: CliRunner):
        self.runner = runner


    def test_basic_cli_command(self):
        result = self.runner.invoke(main)

        assert result.exit_code == 0
        assert result.output is not None


    def test_non_existing_options(self):
        self._assert_exception(self._invoke_main("-d", "nothing"))


    @pytest.mark.parametrize("arg, value", [
        ("-t", "single"),
        ("--type", "single"),
        ("-t", "twopart"),
        ("--type", "twopart")
    ])
    def test_valid_type_options(self, arg: str, value: str):
        self._assert_successful(self._invoke_main(arg, value))


    @pytest.mark.parametrize("arg, value", [
        ("-t", "random"),
        ("--type", "nonexistent")
    ])
    def test_invalid_type_options(self, arg: str, value: str):
        self._assert_exception(self._invoke_main(arg, value))


    @pytest.mark.parametrize("arg, value", [
        ("-c", "any"),
        ("--category", "any"),
        ("-c", "misc"),
        ("--category", "misc"),
        ("-c", "programming"),
        ("--category", "programming"),
        ("-c", "dark"),
        ("--category", "dark"),
        ("-c", "pun"),
        ("--category", "pun"),
        ("-c", "spooky"),
        ("--category", "spooky"),
        ("-c", "christmas"),
        ("--category", "christmas")
    ])
    def test_valid_category_options(self, arg: str, value: str):
        self._assert_successful(self._invoke_main(arg, value))


    @pytest.mark.parametrize("arg, value", [
        ("-c", "random"),
        ("--category", "nonexistent")
    ])
    def test_invalid_category_options(self, arg: str, value: str):
        self._assert_exception(self._invoke_main(arg, value))


    @pytest.mark.parametrize("arg, value", [
        ("-f", "nsfw"),
        ("--flag", "nsfw"),
        ("-f", "religious"),
        ("--flag", "religious"),
        ("-f", "political"),
        ("--flag", "political"),
        ("-f", "racist"),
        ("--flag", "racist"),
        ("-f", "sexist"),
        ("--flag", "sexist"),
        ("-f", "explicit"),
        ("--flag", "explicit")
    ])
    def test_valid_flag_options(self, arg: str, value: str):
        self._assert_successful(self._invoke_main(arg, value))


    @pytest.mark.parametrize("arg, value", [
        ("-f", "random"),
        ("--flag", "nonexistent")
    ])
    def test_invalid_flag_options(self, arg: str, value: str):
        self._assert_exception(self._invoke_main(arg, value))


    def _invoke_main(self, arg: str, value: str) -> Result:
        return self.runner.invoke(main, [arg, value])


    def _assert_successful(self, result: Result) -> None:
        assert result.exception is None
        assert result.output is not None


    def _assert_exception(self, result: Result) -> None:
        assert result.exception is not None

    