import click
from pydantic import ValidationError
import pytest

from jokes.models.responses import ErrorResponse, GetJokeResponse
from jokes.options import Types
from jokes.utils.messages import (
    INTERNAL_JOKE_API_ERROR,
    INVALID_RESPONSE,
    SINGLE_JOKE_ERROR,
    TWOPART_JOKE_ERROR,
)

from .factories import (
    ErrorResponseFactory,
    JokeResponseFactory,
    JokesResponse,
    build_single_joke_response,
    build_twopart_joke_response,
)


# fmt: off
@pytest.mark.parametrize("response", [
    pytest.param(
        JokeResponseFactory.build(type=Types.TWOPART.value, joke=None),
        id="Test joke with only setup and delivery parameters succeeds"
    ),
    pytest.param(
        JokeResponseFactory.build(type=Types.SINGLE.value, setup=None, delivery=None),
        id="Test joke with only joke parameter succeeds"
    )
])
def test_joke_response_succeeds(response: JokesResponse):
    joke_response = GetJokeResponse(**response.dict(exclude_none=True))

    assert joke_response.joke == response.joke
    assert joke_response.setup == response.setup
    assert joke_response.delivery == response.delivery

@pytest.mark.parametrize("response, error_msg", [
    pytest.param(
        JokeResponseFactory.build(type=Types.TWOPART.value),
        TWOPART_JOKE_ERROR,
        id="Twopart joke fails validation when joke in response"
    ),
    pytest.param(
        JokeResponseFactory.build(type=Types.TWOPART.value, delivery=None, joke=None),
        TWOPART_JOKE_ERROR,
        id="Twopart joke fails validation with setup but no delivery"
    ),
    pytest.param(
        JokeResponseFactory.build(type=Types.TWOPART.value, setup=None, joke=None),
        TWOPART_JOKE_ERROR,
        id="Twopart joke fails validation with delivery but no setup"
    ),
    pytest.param(
        JokeResponseFactory.build(type=Types.SINGLE.value, joke=None),
        SINGLE_JOKE_ERROR,
        id="Single joke fails validation with no joke"
    ),
    pytest.param(
        JokeResponseFactory.build(type=Types.SINGLE.value, delivery=None),
        SINGLE_JOKE_ERROR,
        id="Single joke fails validation with joke and setup"
    ),
    pytest.param(
        JokeResponseFactory.build(type=Types.SINGLE.value, setup=None),
        SINGLE_JOKE_ERROR,
        id="Single joke fails validation with joke and delivery"
    ),
    pytest.param(
        JokeResponseFactory.build(type=Types.SINGLE.value),
        SINGLE_JOKE_ERROR,
        id="Single joke fails validation with joke, delivery, and setup"
    ),
    pytest.param(
        JokeResponseFactory.build(),
        INVALID_RESPONSE,
        id="Validation fails with invalid type"
    ),
])
def test_joke_response_fails(response: JokesResponse, error_msg: str):
    with pytest.raises(ValidationError, match=error_msg):
        GetJokeResponse(**response.dict(exclude_none=True))

@pytest.mark.parametrize("response, expected", [
    pytest.param(
        (response := build_single_joke_response()),
        response.joke,
        id="Single joke returns only the joke field"
    ),
    pytest.param(
        (response := build_twopart_joke_response()),
        "\n".join([response.setup, response.delivery]),
        id="Twopart joke returns the joined setup and delivery"
    )
])
def test_extract_joke(response: JokesResponse, expected: str):
    joke_response = GetJokeResponse(**response.dict(exclude_none=True))

    assert joke_response.extract_joke() == expected

@pytest.mark.parametrize("context_obj, expected", [
    pytest.param({"DEBUG": (expected := True)}, expected, id="True when debug is set to true"),
    pytest.param({"DEBUG": (expected := False)}, expected, id="False when debug is set to false"),
    pytest.param({}, False, id="False when no debug in context")
])
def test_debug_property_relies_on_context(context_obj: dict, expected: bool):
    with click.Context(click.Command("joke"), obj=context_obj):
        error = ErrorResponse(**ErrorResponseFactory.build().dict())
        assert error.debug == expected

@pytest.mark.parametrize("response, debug, expected",[
    pytest.param(
        ErrorResponseFactory.build(internalError=True),
        False,
        INTERNAL_JOKE_API_ERROR,
        id="Internal error returns internal joke api error"
    ),
    pytest.param(
        (response := ErrorResponseFactory.build(internalError=False)),
        True,
        "\n".join([response.message, response.additionalInfo] + response.causedBy),
        id="Error with debug and no internal error returns joined messages"
    ),
    pytest.param(
        (response := ErrorResponseFactory.build(internalError=False)),
        False,
        "\n".join(response.causedBy),
        id="Error without debug and no internal error returns only caused by"
    ),
])
def test_error_to_string(response: ErrorResponse, debug: bool, expected: str):
    with click.Context(click.Command("joke"), obj={"DEBUG": debug}):
        assert response.as_string() == expected
# fmt: on
