from typing import TypeVar
from enum import Enum
from jokes.utils.params import GetEndpointParams, SubmitEndpointParams


BASE_URL = "https://v2.jokeapi.dev"

TParam = TypeVar("TParam", GetEndpointParams, SubmitEndpointParams)


class Endpoints(Enum):
    GET = "joke"
    SUBMIT = "submit"


def format_params(params: TParam) -> str:
    """Formats the params into a string usable by the joke api."""

    return "&".join([k if v is None else f"{k}={v}" for k, v in params.dict().items()])


def build_endpoint_url(endpoint: Endpoints, params: TParam) -> str:
    """Builds a valid joke api endpoint url."""

    category = params.category if isinstance(params, GetEndpointParams) else None
    url = "/".join(filter(None, [BASE_URL, endpoint.value, category]))

    return f"{url}?{query_params}" if (query_params := format_params(params)) else url
