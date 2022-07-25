import pytest

from typing import Any
from jokes.models.joke import Joke
from jokes.models.error import Error


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
        joke = Joke(**valid_single_data)

        assert joke.type == valid_single_data["type"]
        assert joke.category == valid_single_data["category"]
        assert joke.joke == valid_single_data["joke"]
        assert joke.delivery == None
        assert joke.setup == None
        assert joke.as_string() == valid_single_data["joke"]


    def test_twopart_joke_success(self, valid_twopart_data: dict[str, Any]):
        joke = Joke(**valid_twopart_data)
        setup = valid_twopart_data["setup"]
        delivery = valid_twopart_data["delivery"]

        assert joke.type == valid_twopart_data["type"]
        assert joke.category == valid_twopart_data["category"]
        assert joke.joke == None
        assert joke.delivery == delivery
        assert joke.setup == setup
        assert joke.as_string() == "\n".join([setup, delivery])


    def test_error_success(self, valid_error_data: dict[str, Any]):
        error = Error(**valid_error_data)

        assert error.message == valid_error_data["message"]
        assert error.additionalInfo == valid_error_data["additionalInfo"]
        assert error.causedBy == valid_error_data["causedBy"]
        assert error.internalError == valid_error_data["internalError"]
        assert error.as_string() == "\n".join(valid_error_data["causedBy"])


    def test_joke_invalid_data(self):
        pass
