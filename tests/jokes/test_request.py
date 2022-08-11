import pytest

from jokes.models import JokeSingle, JokeTwopart
from jokes.options import Language, Type, Flag, Category
from jokes.utils.params import GetEndpointParams
from jokes.pipelines.get_pipeline import make_request, deserialize
from returns.unsafe import unsafe_perform_io


class TestRequest:
    @pytest.mark.parametrize("type, category, flags, lang", [
        (Type.SINGLE, Category.ANY, [Flag.NSFW, Flag.EXPLICIT], Language.EN),
        (Type.SINGLE, Category.DARK, [Flag.NSFW, Flag.EXPLICIT], Language.EN),
        (Type.SINGLE, Category.PROGRAMMING, [Flag.NSFW, Flag.EXPLICIT], Language.EN),
        (Type.TWOPART, Category.ANY, [Flag.NSFW, Flag.EXPLICIT], Language.EN),
        (Type.TWOPART, Category.DARK, [Flag.NSFW, Flag.EXPLICIT], Language.EN),
        (Type.TWOPART, Category.PROGRAMMING, [Flag.NSFW, Flag.EXPLICIT], Language.EN),
    ])
    def test_complete_response(self, type: Type, category: Category, flags: list[Flag], lang: Language):
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
        flags: list[Flag] = [],
        lang: Language = Language.EN
    ) -> GetEndpointParams:
        return GetEndpointParams(
            category=category.name,
            type=type.name,
            flags=[f.name for f in flags],
            lang=lang.name
        )
