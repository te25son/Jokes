from dataclasses import dataclass
from httpx import Response, Client
from returns.io import IOResultE, impure_safe
from returns.result import safe
from returns.pipeline import flow
from returns.pointfree import bind_ioresult, bind_result
from jokes.models.joke import SubmitJoke, SubmittedJokeResponse
from jokes.models.error import Error


@dataclass
class JokeSubmitData:
    type: str
    category: str
    flags: dict[str, bool]
    joke: str | None = None
    setup: str | None = None
    delivery: str | None = None


def submit_joke(data: JokeSubmitData) -> IOResultE[Response]:
    return flow(
        data,
        make_joke,
        bind_ioresult(submit_request),
        bind_result(deserialize_response)
    )


@impure_safe
def make_joke(data: JokeSubmitData) -> str:
    return SubmitJoke(**data.__dict__).json(exclude_none=True)


@impure_safe
def submit_request(data: str) -> Response:
    with Client() as client:
        response = client.post("https://v2.jokeapi.dev/submit?dry-run", json=data)
        response.raise_for_status()

        return response


@safe
def deserialize_response(response: Response) -> SubmittedJokeResponse | Error:
    response_as_json = response.json()
    return SubmittedJokeResponse(**response_as_json) if not response_as_json["error"] else Error(**response_as_json)
