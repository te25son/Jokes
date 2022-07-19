import pytest

from typing import Any
from jokes.joke import Joke
from returns.maybe import Some, Nothing


class TestJoke:
    @pytest.fixture
    def valid_single_data(self) -> dict[str, Any]:
        return {
            'error': False,
            'category': 'Dark',
            'type': 'single',
            'joke': "Some funny joke.",
            'flags': {
                'nsfw': False,
                'religious': False,
                'political': False,
                'racist': False,
                'sexist': False,
                'explicit': False
            }
        }


    @pytest.fixture
    def valid_twopart_data(self) -> dict[str, Any]:
        return {
            'error': False,
            'category': 'Dark',
            'type': 'twopart',
            'setup': "Why did the chicken cross the road?",
            'delivery': "To get to the other side.",
            'flags': {
                'nsfw': False,
                'religious': False,
                'political': False,
                'racist': False,
                'sexist': False,
                'explicit': False
            }
        }


    @pytest.fixture
    def valid_error_data(self) -> dict[str, Any]:
        return {
            'error': True,
            'internalError': False,
            'message': 'No matching joke found',
            'causedBy': ['No jokes were found that match your provided filter(s)'],
            'additionalInfo': 'The specified ID range was out of boungs.'
        }


    def test_single_joke_success(self, valid_single_data: dict[str, Any]):
        joke = Joke.create(valid_single_data)

        assert joke.type == valid_single_data["type"]
        assert joke.category == Some(valid_single_data["category"])
        assert joke.joke == Some(valid_single_data["joke"])
        assert joke.delivery == Nothing
        assert joke.setup == Nothing
        assert str(joke) == valid_single_data["joke"]


    def test_twopart_joke_success(self, valid_twopart_data: dict[str, Any]):
        joke = Joke.create(valid_twopart_data)
        setup = valid_twopart_data["setup"]
        delivery = valid_twopart_data["delivery"]

        assert joke.type == valid_twopart_data["type"]
        assert joke.category == Some(valid_twopart_data["category"])
        assert joke.joke == Nothing
        assert joke.delivery == Some(valid_twopart_data["delivery"])
        assert joke.setup == Some(valid_twopart_data["setup"])
        assert str(joke) == "\n".join([setup, delivery])


    def test_error_success(self, valid_error_data: dict[str, Any]):
        joke = Joke.create(valid_error_data)

        assert joke.type == None
        assert joke.category == Nothing
        assert joke.joke == Nothing
        assert joke.delivery == Nothing
        assert joke.setup == Nothing
        assert joke.error.message == Some(valid_error_data["message"])
        assert joke.error.additionalInfo == Some(valid_error_data["additionalInfo"])
        assert joke.error.causedBy == Some(valid_error_data["causedBy"])
        assert joke.error.internalError == valid_error_data["internalError"]
        assert str(joke) == "\n".join(valid_error_data["causedBy"])


    def test_joke_invalid_data(self):
        joke = Joke.create({})

        assert joke.type == None
        assert joke.category == Nothing
        assert joke.joke == Nothing
        assert joke.delivery == Nothing
        assert joke.setup == Nothing
        assert joke.error.internalError == False
        assert joke.error.additionalInfo == Nothing
        assert joke.error.causedBy == Nothing
        assert joke.error.message == Nothing
        assert str(joke) == "An unexpected error occurred."
