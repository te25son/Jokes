from pydantic import BaseModel
from pydantic_factories import ModelFactory

from jokes.models import ErrorResponse, Flags, GetEndpointParams
from jokes.options import Types

# MODELS ================================


class JokesResponse(BaseModel):
    error: bool
    category: str
    type: str
    flags: Flags
    id: int
    safe: bool
    lang: str
    joke: str | None
    setup: str | None
    delivery: str | None


# FACTORIES ==============================


class JokeResponseFactory(ModelFactory):
    __model__ = JokesResponse
    __allow_none_optionals__ = False


class ErrorResponseFactory(ModelFactory):
    __model__ = ErrorResponse


class GetEndpointParamsFactory(ModelFactory):
    __model__ = GetEndpointParams
    __allow_none_optionals__ = False


# HELPERS =================================


def build_single_joke_response() -> JokesResponse:
    return JokeResponseFactory.build(error=False, type=Types.SINGLE.value, setup=None, delivery=None)


def build_twopart_joke_response() -> JokesResponse:
    return JokeResponseFactory.build(error=False, type=Types.TWOPART.value, joke=None)
