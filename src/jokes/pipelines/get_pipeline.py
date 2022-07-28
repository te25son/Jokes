from jokes.options import OptionData
from httpx import Response, Client
from returns.io import IOResultE, impure_safe
from returns.result import safe
from returns.pipeline import flow
from returns.pointfree import bind_result
from jokes.models.joke import Joke
from jokes.models.error import Error


def get_joke(data: OptionData) -> IOResultE[str]:
    """Flow/Pipeline for safely getting a joke from the JokeAPI"""

    return flow(
        data,
        make_request,
        bind_result(deserialize),
        bind_result(get_content)
    )


@impure_safe
def make_request(data: OptionData) -> Response:
    """
    Makes a GET request to the Joke API /joke endpoint.
    Raises an error if the response's status code is not 200
    """

    params = dict(
        type = data.type,
        blacklistFlags = "+".join(data.flags)
    )
    with Client(params=params) as client:
        response = client.get(f"https://v2.jokeapi.dev/joke/{data.category}")
        response.raise_for_status()

        return response


@safe
def deserialize(response: Response) -> Joke | Error:
    """Safely deserializes the API response."""

    response_data: dict = response.json()
    is_error: bool = response_data["error"]

    return Joke(**response_data) if not is_error else Error(**response_data)


@safe
def get_content(model: Joke | Error) -> str:
    """Safely gets the content of the deserialized object."""

    return model.as_string()
