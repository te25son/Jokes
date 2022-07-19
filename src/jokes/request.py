from jokes.options import OptionData
from httpx import Response, Client
from returns.io import IOResultE, impure_safe
from returns.result import safe
from returns.pipeline import flow
from returns.pointfree import bind_result
from jokes.joke import Joke


def get_joke(data: OptionData) -> IOResultE[str]:
    return flow(
        data,
        _make_request,
        bind_result(_deserialize),
        bind_result(_get_content)
    )


@impure_safe
def _make_request(data: OptionData) -> Response:
    params = {
        "type": data.type,
        "blacklistFlags": "+".join(data.flags)
    }
    with Client(params=params) as client:
        response = client.get(f"https://v2.jokeapi.dev/joke/{data.category}")
        response.raise_for_status()

        return response


@safe
def _deserialize(response: Response) -> Joke:
    return Joke.create(response.json())


@safe
def _get_content(joke: Joke) -> str:
    return str(joke)
    