import pytest

from jokes.models import JokeSingle, JokeTwopart
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

        match type:
            case Type.SINGLE:
                assert isinstance(response, JokeSingle)
                assert response.joke is not None
            case Type.TWOPART: 
                assert isinstance(response, JokeTwopart)
                assert response.setup is not None
                assert response.delivery is not None


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
