import pytest
from jokes.models.joke import Joke
from jokes.options import OptionData, Type, Flag, Category
from jokes.request import make_request, deserialize
from returns.unsafe import unsafe_perform_io


class TestRequest:
    @pytest.mark.parametrize("type", [
        Type.SINGLE,
        Type.TWOPART
    ])
    def test_type_option_creates_correct_response(self, type: Type):
        data = self._create_option_data(type=type)
        response = unsafe_perform_io(make_request(data).bind_result(deserialize).unwrap())

        assert isinstance(response, Joke)
        assert response.type == type.name.lower()


    @staticmethod
    def _create_option_data(
        category: Category = Category.ANY,
        type: Type = Type.SINGLE,
        flags: list[Flag] = []
    ) -> OptionData:
        return OptionData(
            category=category.name.lower(),
            type=type.name.lower(),
            flags=[f.name.lower() for f in flags]
        )