import click
import pytest

from jokes.options import Categories, Flags, Languages, Types
from jokes.utils.urls import BASE_URL, Endpoints, build_endpoint_url

from .factories import GetEndpointParamsFactory


class TestUrls:
    @pytest.mark.parametrize(
        "type, category, lang, flags, safe, expected",
        [
            pytest.param(
                Types.SINGLE,
                Categories.ANY,
                Languages.EN,
                [Flags.NSFW, Flags.EXPLICIT, Flags.POLITICAL],
                False,
                "/joke/ANY?type=SINGLE&lang=EN&blacklistFlags=NSFW+EXPLICIT+POLITICAL",
                id="Test multiple flags",
            ),
            pytest.param(
                Types.TWOPART,
                Categories.DARK,
                Languages.FR,
                [Flags.SEXIST],
                False,
                "/joke/DARK?type=TWOPART&lang=FR&blacklistFlags=SEXIST",
                id="Test single flag",
            ),
            pytest.param(
                Types.SINGLE,
                Categories.PROGRAMMING,
                Languages.PT,
                [],
                False,
                "/joke/PROGRAMMING?type=SINGLE&lang=PT",
                id="Test no flags",
            ),
            pytest.param(
                Types.SINGLE,
                Categories.PUN,
                Languages.ES,
                [Flags.NSFW],
                True,
                "/joke/PUN?type=SINGLE&lang=ES&blacklistFlags=NSFW&safe-mode",
                id="Test with safe mode",
            ),
        ],
    )
    def test_get_endpoint_url(
        self,
        type: Types,
        category: Categories,
        lang: Languages,
        flags: list[Flags],
        safe: bool,
        expected: str,
    ) -> None:
        """Test that the get endpoint is created correctly."""

        with click.Context(click.Command("joke"), obj={"SAFE_MODE": safe}):
            params = GetEndpointParamsFactory.build(
                type=type.name,
                category=category.name,
                lang=lang.name,
                blacklist_flags=[f.name for f in flags],
                safe_mode=None,
            )
            url = build_endpoint_url(Endpoints.GET, params)

            assert url == f"{BASE_URL}{expected}"
