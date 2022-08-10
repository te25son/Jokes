from jokes.options import OptionData
from httpx import Response, Client
from returns.io import IOResultE, impure_safe
from returns.result import safe
from returns.pipeline import flow
from returns.pointfree import bind_result
from jokes.utils.urls import GetEndpointParams, Endpoints, build_endpoint_url
from jokes.models import (
    APIResponse,
    JokeBase,
    JokeSingle,
    JokeTwopart,
    Joke,
    JokeE
)


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

    params = GetEndpointParams(
        category=data.category,
        type=data.type,
        blacklistFlags = "+".join(data.flags)
    )

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
        twopart_action=lambda d: JokeTwopart(**d)
    )


@safe
def get_content(model: JokeE) -> str:
    """Safely gets the content of the deserialized object."""

    return str(model)
