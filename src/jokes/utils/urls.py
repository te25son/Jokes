from enum import Enum
from typing import Mapping

from jokes.models import GetEndpointParams

BASE_URL = "https://v2.jokeapi.dev"

Primitive = str | int | float | bool | None


class Endpoints(Enum):
    GET = "joke"
    SUBMIT = "submit"


def build_query_string(dict: Mapping[str, Primitive]) -> str:
    """
    Formats the params into a string usable by the joke api.
    """
    return "&".join([k if v is None else f"{k}={v}" for k, v in dict.items()])


def build_endpoint_url(endpoint: Endpoints, params: GetEndpointParams) -> str:
    """
    Builds a valid joke api endpoint url.
    """
    url = "/".join(filter(None, [BASE_URL, endpoint.value, params.category]))

    return (
        f"{url}?{query_string}"
        if (query_string := build_query_string(params.to_filtered_dict()))
        else url
    )
