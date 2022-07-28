from httpx import Response, Client
from returns.io import IOResultE, impure_safe
from returns.result import safe
from returns.pipeline import flow
from returns.pointfree import bind_ioresult, bind_result
from jokes.models.joke import SubmitJoke, SubmittedJoke
from jokes.models.error import Error


def submit_joke(data: dict) -> IOResultE[Response]:
    """Flow/Pipeline for safely submitting a joke to the JokeAPI"""

    return flow(
        data,
        validate_and_format_joke,
        bind_ioresult(submit_request),
        bind_result(deserialize)
    )


@impure_safe
def validate_and_format_joke(data: dict) -> str:
    """Validates and formats the joke into a json object."""

    return SubmitJoke(**data).json(exclude_none=True)


@impure_safe
def submit_request(data: str) -> Response:
    """
    Submits a json object string to the Joke API submit endpoint.
    Raises an error if the response's status code is not 200.
    """

    with Client() as client:
        response = client.post("https://v2.jokeapi.dev/submit?dry-run", json=data)
        response.raise_for_status()

        return response


@safe
def deserialize(response: Response) -> SubmittedJoke | Error:
    """Safely deserializes the API response."""

    response_data = response.json()
    is_error = response_data["error"]

    return SubmittedJoke(**response_data) if not is_error else Error(**response_data)
