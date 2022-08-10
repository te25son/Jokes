from typing import Mapping
from enum import Enum
from jokes.utils.params import GetEndpointParams, SubmitEndpointParams


BASE_URL = "https://v2.jokeapi.dev"

Primitive = str | int | float | bool | None
TParam = GetEndpointParams | SubmitEndpointParams


class Endpoints(Enum):
    GET = "joke"
    SUBMIT = "submit"


def build_query_string(dict: Mapping[str, Primitive]) -> str:
    """Formats the params into a string usable by the joke api."""

    return "&".join([k if v is None else f"{k}={v}" for k, v in dict.items()])


def build_endpoint_url(endpoint: Endpoints, params: TParam) -> str:
    """Builds a valid joke api endpoint url."""

    category = params.category if isinstance(params, GetEndpointParams) else None
    url = "/".join(filter(None, [BASE_URL, endpoint.value, category]))

    return f"{url}?{query_string}" if (query_string := build_query_string(params.dict())) else url
