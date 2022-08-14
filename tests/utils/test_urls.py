import pytest

from jokes.options import Type, Category, Language, Flag
from jokes.utils.urls import build_endpoint_url, Endpoints, BASE_URL
from jokes.utils.params import GetEndpointParams, SubmitEndpointParams


class TestUrls:
    """Class for testing urls."""


    @pytest.mark.parametrize("type, category, lang, flags, expected", [
        (
            Type.SINGLE, Category.ANY, Language.EN, [Flag.NSFW, Flag.EXPLICIT, Flag.POLITICAL],
            "/joke/ANY?type=SINGLE&lang=EN&blacklistFlags=NSFW+EXPLICIT+POLITICAL"
        ),
        (
            Type.TWOPART, Category.DARK, Language.FR, [Flag.SEXIST],
            "/joke/DARK?type=TWOPART&lang=FR&blacklistFlags=SEXIST"
        ),
        (
            Type.SINGLE, Category.PROGRAMMING, Language.PT, [],
            "/joke/PROGRAMMING?type=SINGLE&lang=PT"
        )
    ])
    def test_get_endpoint_url(self, type: Type, category: Category, lang: Language, flags: list[Flag], expected: str):
        """"Test that the get endpoint is created correctly."""

        params = GetEndpointParams(
            type=type.name,
            category=category.name,
            lang=lang.name,
            blacklist_flags=[f.name for f in flags]
        )
        url = build_endpoint_url(Endpoints.GET, params)

        assert url == f"{BASE_URL}{expected}"


    def test_submit_endpoint_url(self):
        """Test that the submit endpoint is created correctly."""

        url = build_endpoint_url(Endpoints.SUBMIT, SubmitEndpointParams())

        assert url == f"{BASE_URL}/submit"


        