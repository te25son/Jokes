from click import get_current_context
from pydantic import BaseModel, root_validator

from jokes.models import Flags
from jokes.options import Types
from jokes.utils.messages import (
    INTERNAL_JOKE_API_ERROR,
    INVALID_RESPONSE,
    SINGLE_JOKE_ERROR,
    TWOPART_JOKE_ERROR,
)


class ErrorResponse(BaseModel):
    internalError: bool
    message: str
    causedBy: list[str]
    additionalInfo: str

    @property
    def debug(self) -> bool:
        """
        Gets the 'Debug' value from the current thread's context if it exists. If neither
        the thread nor the value exist, returns False.
        """
        return (
            context.obj.get("DEBUG", False)
            if (context := get_current_context(silent=True))
            else False
        )

    def as_string(self) -> str:
        """
        Return error as a string depending on whether or not the debug flag has been set
        or not.
        """
        if self.internalError:
            return INTERNAL_JOKE_API_ERROR
        if self.debug:
            return "\n".join([self.message, self.additionalInfo] + self.causedBy)
        return "\n".join(self.causedBy)


class GetJokeResponse(BaseModel):
    category: str
    type: str
    flags: Flags
    id: int
    safe: bool
    lang: str
    joke: str | None = None
    setup: str | None = None
    delivery: str | None = None

    @root_validator(pre=True)
    def check_joke_type_contains_correct_properties(cls, values: dict) -> dict:
        """
        Check that the joke type contains the correct content. A single type
        joke should only contain the joke property and neither delivery nor setup.
        A twopart joke should contain both delivery and setup and no joke.
        """
        joke_type = values.get("type", "").lower()
        if joke_type == Types.SINGLE.value:
            assert "joke" in values and (
                "setup" not in values and "delivery" not in values
            ), SINGLE_JOKE_ERROR
            return values
        if joke_type == Types.TWOPART.value:
            assert "joke" not in values and (
                "setup" in values and "delivery" in values
            ), TWOPART_JOKE_ERROR
            return values
        raise ValueError(INVALID_RESPONSE)

    def extract_joke(self) -> str:
        """
        Extracts the joke from the response in the form of a string.
        """
        # There are only two possible values (single, twopart) since this is checked
        # in the validation
        if self.type.lower() == Types.SINGLE.value:
            return self.joke
        return "\n".join([self.setup, self.delivery])
