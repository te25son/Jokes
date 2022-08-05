from typing import Callable, Any
from jokes.options import Type
from jokes.models.flags import Flags
from pydantic import root_validator, BaseModel, validator
from returns.maybe import Maybe


class Joke(BaseModel):
    """
    Base joke class with validation. Also used for
    deserializing the response of the `get` endpoint.
    """

    type: str
    category: str
    setup: str | None = None
    delivery: str | None = None
    joke: str | None = None


    @validator('type', 'category', pre=True)
    def to_upper(cls, value: str) -> str:
        """Converts the incoming fields to uppercase."""

        return value.upper()


    @root_validator()
    def check_valid_joke(cls, values: dict[Any, str]) -> dict[Any, str]:
        """Validates that the incoming joke data is valid based on the given type."""

        get_value: Callable[[str], str | None] = lambda v: values.get(v)

        type = Type[value] if (value := get_value("type")) else None
        setup, delivery, joke = get_value("setup"), get_value("delivery"), get_value("joke")

        match type:
            case Type.TWOPART:
                assert setup is not None, "Setup field must be included in a twopart joke."
                assert delivery is not None, "Delivery field must be included in a twopart joke."
                assert joke is None, "Joke field cannot be included in a twopart joke."

            case Type.SINGLE:
                assert setup is None, "Setup field cannot be included in a single joke."
                assert delivery is None, "Delivery field cannot be included in a single joke."
                assert joke is not None, "Joke field must be included in a single joke."

            case _:
                raise ValueError(f"Invalid type.")

        return values


    def get_joke_by_type(self) -> Maybe[str]:
        """Gets the joke by the type and wraps it in a container."""

        safe: Callable[[str | None], Maybe[str]] = lambda v: Maybe.from_optional(v)

        match Type[self.type]:
            case Type.SINGLE:
                return safe(self.joke)

            case Type.TWOPART:
                return Maybe.do(
                    "\n".join([s, d])
                    for s in safe(self.setup)
                    for d in safe(self.delivery)
                )

            case _:
                return Maybe.empty


    def as_string(self) -> str:
        """
        Unwraps the joke and returns the value or a
        default message if the joke does not exist.
        """

        return self.get_joke_by_type().value_or(f"Could not find joke with type: '{self.type}'.")


class SubmitJoke(Joke):
    """Class for creating the data necessary to submit a joke."""

    formatVersion: int = 3
    lang: str = "en"
    flags: Flags


class SubmittedJoke(BaseModel):
    """Class for deserializing the response of a submitted joke."""

    message: str
