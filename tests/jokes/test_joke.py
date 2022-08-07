import pytest
import string
import typing

from types import SimpleNamespace
from pydantic import ValidationError
from jokes.options import Category, Type
from jokes.models import (
    JokeBase,
    JokeSubmit,
    JokeSingle,
    JokeTwopart,
    JokeSingleSubmit,
    JokeTwopartSubmit,
    JokeSubmitted,
    Error
)



class TestJoke:
    @pytest.fixture
    def simple_joke_data(self) -> SimpleNamespace:
        return SimpleNamespace(
            type=Type.SINGLE.name,
            category=Category.DARK.name
        )

    @pytest.fixture
    def valid_single_joke_get_response(self) -> dict[str, typing.Any]:
        return {
            "error": False,
            "category": Category.DARK.name,
            "type": Type.SINGLE.name,
            "joke": "Some funny joke.",
            "flags": {
                "nsfw": False,
                "religious": False,
                "political": False,
                "racist": False,
                "sexist": False,
                "explicit": False
            }
        }


    @pytest.fixture
    def valid_twopart_joke_get_response(self) -> dict[str, typing.Any]:
        return {
            "error": False,
            "category": Category.DARK.name,
            "type": Type.TWOPART.name,
            "setup": "Why did the chicken cross the road?",
            "delivery": "To get to the other side.",
            "flags": {
                "nsfw": False,
                "religious": False,
                "political": False,
                "racist": False,
                "sexist": False,
                "explicit": False
            }
        }


    @pytest.fixture
    def valid_error_response(self) -> dict[str, typing.Any]:
        return {
            'error': True,
            'internalError': False,
            'message': 'No matching joke found',
            'causedBy': ['No jokes were found that match your provided filter(s)'],
            'additionalInfo': 'The specified ID range was out of boungs.'
        }


    def test_joke_base_includes_all_data(self, valid_single_joke_get_response: dict[str, typing.Any]):
        joke = JokeBase(**valid_single_joke_get_response)

        assert joke.dict() == valid_single_joke_get_response


    def test_single_joke_success(self, valid_single_joke_get_response: dict[str, typing.Any]):
        joke = JokeSingle(**valid_single_joke_get_response)

        assert joke.joke == valid_single_joke_get_response["joke"]
        assert str(joke) == valid_single_joke_get_response["joke"]


    def test_twopart_joke_success(self, valid_twopart_joke_get_response: dict[str, typing.Any]):
        joke = JokeTwopart(**valid_twopart_joke_get_response)
        setup = valid_twopart_joke_get_response["setup"]
        delivery = valid_twopart_joke_get_response["delivery"]

        assert joke.delivery == delivery
        assert joke.setup == setup
        assert str(joke) == "\n".join([setup, delivery])


    def test_error_success(self, valid_error_response: dict[str, typing.Any]):
        error = Error(**valid_error_response)

        assert error.message == valid_error_response["message"]
        assert error.additionalInfo == valid_error_response["additionalInfo"]
        assert error.causedBy == valid_error_response["causedBy"]
        assert error.internalError == valid_error_response["internalError"]
        assert str(error) == "\n".join(valid_error_response["causedBy"])


    def test_error_invalid_data(self):
        with pytest.raises(ValidationError) as ex:
            Error(**{})


    @pytest.mark.parametrize("joke_class", [
        JokeSingle,
        JokeTwopart,
        JokeBase,
        JokeSingleSubmit,
        JokeTwopartSubmit,
        JokeSubmitted,
        JokeSubmit
    ])
    def test_joke_invalid_data(self, joke_class: typing.Type):
        with pytest.raises(ValidationError):
            joke_class(**{})


    @pytest.mark.parametrize("joke_class", [JokeTwopart, JokeTwopartSubmit])
    def test_cannot_create_twopart_joke_without_setup_and_delivery(self, joke_class: typing.Type, simple_joke_data: SimpleNamespace):
        simple_joke_data.type = Type.TWOPART.name

        with pytest.raises(ValidationError):
            joke_class(**simple_joke_data.__dict__)


    @pytest.mark.parametrize("joke_class", [JokeTwopart, JokeTwopartSubmit])
    def test_cannot_create_twopart_joke_with_setup_but_no_delivery(self, joke_class: typing.Type, simple_joke_data: SimpleNamespace):
        simple_joke_data.type = Type.TWOPART.name
        simple_joke_data.setup = string.ascii_letters

        with pytest.raises(ValidationError):
            joke_class(**simple_joke_data.__dict__)


    @pytest.mark.parametrize("joke_class", [JokeSingle, JokeSingleSubmit])
    def test_cannot_create_single_joke_without_joke_field(self, joke_class: typing.Type, simple_joke_data: SimpleNamespace):
        with pytest.raises(ValidationError):
            joke_class(**simple_joke_data.__dict__)
