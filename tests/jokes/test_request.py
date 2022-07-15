import pytest

from jokes.options import OptionData, Type, Flag, Category
from jokes.request import _make_request, _deserialize
from returns.unsafe import unsafe_perform_io


class TestRequest:
    @pytest.mark.parametrize("type", [
        Type.SINGLE,
        Type.TWOPART
    ])
    def test_type_option_creates_correct_response(self, type: Type):
        data = self._create_option_data(type=type)
        response = unsafe_perform_io(_make_request(data).bind_result(_deserialize).unwrap())

        assert response.type == type.name.lower()
        assert response.error == False


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