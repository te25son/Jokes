from typing import Mapping
from enum import Enum


Primitive = str | int | float | bool | None

BASE_URL = "https://v2.jokeapi.dev"


class Endpoints(Enum):
    GET = "joke"
    SUBMIT = "submit"


class URLBuilder:
    """Class for building joke api urls."""


    @classmethod
    def build_get_endpoint(cls, category: str, params: Mapping[str, Primitive] = None) -> str:
        """Builds the joke api get endpoint."""

        return cls._build(Endpoints.GET, category, params)


    @classmethod
    def build_submit_endpoint(cls, params: Mapping[str, Primitive] = None) -> str:
        """Builds the joke api submit endpoint."""

        return cls._build(Endpoints.SUBMIT, params=params)


    @classmethod
    def _build(
        cls,
        endpoint: Endpoints,
        category: str | None = None,
        params: Mapping[str, Primitive] = None
    ) -> str:
        """Builds a valid joke api endpoint url."""

        url = "/".join(filter(None, [BASE_URL, endpoint.value, category]))

        return f"{url}?{cls._format_params(params)}" if params else url


    @staticmethod
    def _format_params(params: Mapping[str, Primitive]) -> str:
        """Formats the params into a string usable by the joke api."""

        return "&".join([k if v is None else f"{k}={v}" for k, v in params.items()])
