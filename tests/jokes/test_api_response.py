import pytest
import typing

from jokes.options import Category, Type
from jokes.models import APIResponse


class TestApiResponse:
    @pytest.fixture
    def valid_data(self) -> dict[str, typing.Any]:
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


    def test_api_response_includes_all_data(self, valid_data: dict[str, typing.Any]):
        response = APIResponse(**valid_data)

        assert response.dict() == valid_data
