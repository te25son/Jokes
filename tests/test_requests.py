import pytest
from pytest_httpx import HTTPXMock

from jokes.models import GetEndpointParams
from jokes.options import Types
from jokes.requests import get_joke
from jokes.utils.messages import UNEXPECTED_ERROR

from .factories import (
    ErrorResponseFactory,
    GetEndpointParamsFactory,
    build_single_joke_response,
    build_twopart_joke_response,
)


# fmt: off
class TestRequests:
    @pytest.fixture(autouse=True)
    def set_common_fixtures(self, httpx_mock: HTTPXMock):
        self.mocker = httpx_mock

    @pytest.mark.parametrize("status_code", [
        pytest.param((code := 400), id=f"Invalid {code}"),
        pytest.param((code := 404), id=f"Invalid {code}"),
        pytest.param((code := 500), id=f"Invalid {code}")
    ])
    def test_get_joke_fails_with_status_code(self, status_code: int):
        self.mocker.add_response(status_code=status_code)
        with pytest.raises(Exception, match=UNEXPECTED_ERROR):
            get_joke(GetEndpointParamsFactory.build(factory_use_construct=True))

    @pytest.mark.parametrize("params", [
        pytest.param(
            GetEndpointParamsFactory.build(type=Types.SINGLE.value, factory_use_construct=True),
            id="Test single joke response succeeds"
        ),
        pytest.param(
            GetEndpointParamsFactory.build(type=Types.TWOPART.value, factory_use_construct=True),
            id="Test twopart joke response succeeds"
        ),
        pytest.param(
            GetEndpointParamsFactory.build(factory_use_construct=True),
            id="Test error joke response succeeds"
        ),
    ])
    def test_get_joke_succeeds(self, params: GetEndpointParams):
        if params.type == Types.SINGLE.value:
            response = build_single_joke_response().dict(exclude_none=True)
        elif params.type == Types.TWOPART.value:
            response = build_twopart_joke_response().dict(exclude_none=True)
        else:
            response = ErrorResponseFactory.build().dict()
            response.update(error=True)

        self.mocker.add_response(json=response)

        get_joke(params)
# fmt: on
