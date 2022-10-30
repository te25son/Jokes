import click
from pydantic_factories import ModelFactory
import pytest
from pytest_httpx import HTTPXMock

from jokes.models.error import INTERNAL_JOKE_API_ERROR, Error


class ErrorFactory(ModelFactory):
    __model__ = Error


class TestModels:
    @pytest.fixture(autouse=True)
    def set_common_fixtures(self, httpx_mock: HTTPXMock):
        self.mocker = httpx_mock

    @pytest.mark.parametrize(
        "obj, expected",
        [
            pytest.param({"DEBUG": True}, True, id="Debug set to true."),
            pytest.param({"DEBUG": False}, False, id="Debug set to false."),
            pytest.param({"NOTHERE": None}, False, id="No debug in context."),
        ],
    )
    def test_error_debug_with_context(self, obj: dict, expected: bool):
        context = click.Context(click.Command("joke"), obj=obj)

        with context:
            error = ErrorFactory.build()
            assert error.debug == expected

    def test_error_debug_without_context(self):
        assert ErrorFactory.build().debug == False

    @pytest.mark.parametrize(
        "is_internal_error, debug",
        [
            pytest.param(True, False, id="Is internal error without debug mode."),
            pytest.param(True, True, id="Is internal error with debug mode."),
            pytest.param(False, False, id="Is not internal error without debug mode."),
            pytest.param(False, True, id="Is not internal error with debug mode."),
        ],
    )
    def test_error_to_string(self, is_internal_error: bool, debug: bool):
        context = click.Context(click.Command("joke"), obj={"DEBUG": debug})

        with context:
            error = ErrorFactory.build(internalError=is_internal_error)
            error_as_str = str(error)

            if is_internal_error:
                assert error_as_str == INTERNAL_JOKE_API_ERROR
            elif debug:
                assert error_as_str == "\n".join(
                    [error.message, error.additionalInfo] + error.causedBy
                )
            else:
                assert error_as_str == "\n".join(error.causedBy)
