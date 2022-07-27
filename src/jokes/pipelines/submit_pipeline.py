from httpx import Response, Client
from returns.io import IOResultE, impure_safe
from returns.result import safe
from returns.pipeline import flow
from returns.pointfree import bind_ioresult, bind_result
from jokes.models.joke import SubmitJoke, SubmittedJoke
from jokes.models.error import Error


def submit_joke(data: SubmitJoke) -> IOResultE[Response]:
    """Flow/Pipeline for safely submitting a joke to the JokeAPI"""

    return flow(
        data,
        joke_to_json,
        bind_ioresult(submit_request),
        bind_result(deserialize)
    )


@impure_safe
def joke_to_json(data: SubmitJoke) -> str:
    return data.json(exclude_none=True)


@impure_safe
def submit_request(data: str) -> Response:
    with Client() as client:
        response = client.post("https://v2.jokeapi.dev/submit?dry-run", json=data)
        response.raise_for_status()

        return response


@safe
def deserialize(response: Response) -> SubmittedJoke | Error:
    response_as_json = response.json()
    is_error = response_as_json["error"]

    return SubmittedJoke(**response_as_json) if not is_error else Error(**response_as_json)
