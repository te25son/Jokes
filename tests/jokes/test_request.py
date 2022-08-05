import pytest
from jokes.models.joke import Joke
from jokes.options import OptionData, Type, Flag, Category
from jokes.pipelines.get_pipeline import make_request, deserialize
from returns.unsafe import unsafe_perform_io


class TestRequest:
    @pytest.mark.parametrize("type, category", [
        (Type.SINGLE, Category.ANY),
        (Type.SINGLE, Category.DARK),
        (Type.SINGLE, Category.PROGRAMMING),
        (Type.TWOPART, Category.ANY),
        (Type.TWOPART, Category.DARK),
        (Type.TWOPART, Category.PROGRAMMING),
    ])
    def test_type_option_creates_correct_response(self, type: Type, category: Category):
        data = self._create_option_data(category, type)
        response = unsafe_perform_io(make_request(data).bind_result(deserialize).unwrap())

        assert isinstance(response, Joke)
        assert response.type == type.name

        if category != Category.ANY:
            assert response.category == category.name


    @staticmethod
    def _create_option_data(
        category: Category,
        type: Type,
        flags: list[Flag] = []
    ) -> OptionData:
        return OptionData(
            category=category.name,
            type=type.name,
            flags=[f.name for f in flags]
        )
