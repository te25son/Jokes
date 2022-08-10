from httpx import Response, Client
from returns.io import IOResultE, impure_safe
from returns.result import safe
from returns.pipeline import flow
from returns.pointfree import bind_ioresult, bind_result
from jokes.utils.urls import build_endpoint_url, Endpoints
from jokes.utils.params import SubmitEndpointParams
from jokes.models import (
    APIResponse,
    JokeBase,
    JokeSingleSubmit,
    JokeTwopartSubmit,
    JokeSubmitted,
    SubmitJoke,
    SubmittedJokeE
)


def submit_joke(data: dict) -> IOResultE[Response]:
    """Flow/Pipeline for safely submitting a joke to the JokeAPI"""

    return flow(
        data,
        serialize,
        bind_ioresult(submit_request),
        bind_result(deserialize)
    )


@impure_safe
def serialize(data: dict) -> str:
    """Serializes the data into a valid json object."""

    return serliaize_joke(data).json(exclude_none=True)


def serliaize_joke(data: dict) -> SubmitJoke:
    """Serializes the data into its proper joke type."""

    joke = JokeBase(**data)

    return joke.match_type(
        single_action=lambda d: JokeSingleSubmit(**d),
        twopart_action=lambda d: JokeTwopartSubmit(**d),
    )


@impure_safe
def submit_request(data: str) -> Response:
    """
    Submits a json object string to the Joke API submit endpoint.
    Raises an error if the response's status code is not 200.
    """

    with Client() as client:
        response = client.post(build_endpoint_url(Endpoints.SUBMIT, SubmitEndpointParams()), json=data)
        response.raise_for_status()

        return response


@safe
def deserialize(response: Response) -> SubmittedJokeE:
    """Safely deserializes the API response."""

    response_data = APIResponse(**response.json())

    return response_data.match_error(if_false=lambda d: JokeSubmitted(**d))
