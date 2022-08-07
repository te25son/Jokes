from pydantic import BaseModel, Extra
from typing import TypeVar, Callable
from jokes.models import Error


T = TypeVar("T", bound=BaseModel)


class APIResponse(BaseModel):
    """Class representing the primary fields of all responses from Joke API."""

    error: bool


    def match_error(
        self,
        *,
        if_true: Callable[[dict], Error] = lambda d: Error(**d),
        if_false: Callable[[dict], T]
    ) -> T | Error:
        """Matches the error of the api response with the given function."""

        data = self.dict()

        return if_true(data) if self.error else if_false(data)


    class Config:
        extra = Extra.allow
