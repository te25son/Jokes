from httpx import Client

from jokes.models import ErrorResponse, GetEndpointParams, GetJokeResponse
from jokes.utils.messages import UNEXPECTED_ERROR
from jokes.utils.urls import Endpoints, build_endpoint_url


def get_joke(params: GetEndpointParams) -> str:
    """
    Creates a request to the `/joke` endpoint and extracts
    the resulting joke from the response.
    """
    with Client() as client:
        response = client.get(build_endpoint_url(Endpoints.GET, params))

        if response.status_code == 200:
            data = response.json()

            if not data["error"]:
                joke_response = GetJokeResponse(**data)
                return joke_response.extract_joke()

            error = ErrorResponse(**data)
            return error.as_string()

    raise Exception(UNEXPECTED_ERROR)
