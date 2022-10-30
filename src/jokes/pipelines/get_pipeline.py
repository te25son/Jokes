from httpx import Client, Response
from returns.io import IOResultE, impure_safe
from returns.pipeline import flow
from returns.pointfree import bind_result
from returns.result import safe

from jokes.models import (
    APIResponse,
    Joke,
    JokeBase,
    JokeE,
    JokeSingle,
    JokeTwopart,
)
from jokes.utils.urls import Endpoints, GetEndpointParams, build_endpoint_url


def get_joke(params: GetEndpointParams) -> IOResultE[str]:
    """Flow/Pipeline for safely getting a joke from the JokeAPI"""

    return flow(
        params, make_request, bind_result(deserialize), bind_result(get_content)
    )


@impure_safe
def make_request(params: GetEndpointParams) -> Response:
    """
    Makes a GET request to the Joke API /joke endpoint.
    Raises an error if the response's status code is not 200
    """

    with Client() as client:
        response = client.get(build_endpoint_url(Endpoints.GET, params))
        response.raise_for_status()

        return response


@safe
def deserialize(response: Response) -> JokeE:
    """Safely deserializes the API response."""

    response_data = APIResponse(**response.json())

    return response_data.match_error(if_false=deserialize_joke)


def deserialize_joke(data: dict) -> Joke:
    """Deserializes the joke into its proper type."""

    joke = JokeBase(**data)

    return joke.match_type(
        single_action=lambda d: JokeSingle(**d),
        twopart_action=lambda d: JokeTwopart(**d),
    )


@safe
def get_content(model: JokeE) -> str:
    """Safely gets the content of the deserialized object."""

    return str(model)
