from jokes.options import Type
from jokes.models.flags import Flags
from pydantic import validator, BaseModel
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


    @property
    def joke_by_type(self) -> dict[str, Maybe[str]]:
        return {
            Type.SINGLE.name.lower(): Maybe.from_optional(self.joke),
            Type.TWOPART.name.lower(): Maybe.do(
                "\n".join([s, d])
                for s in Maybe.from_optional(self.setup)
                for d in Maybe.from_optional(self.delivery)
            )
        }


    @validator("setup", "delivery")
    def setup_and_delivery_can_only_be_defined_with_twopart_type(cls, v: str, values: dict):
        return cls._check_value_should_exist_for_type(
            value=v,
            values=values,
            type=Type.TWOPART,
            error_message="""
                Setup and delivery can only be defined in a twopart joke. All
                twopart jokes must contain both a setup and delivery.
            """
        )


    @validator("joke")
    def joke_can_only_be_defined_with_single_type(cls, v: str, values: dict):
        return cls._check_value_should_exist_for_type(
            value=v,
            values=values,
            type=Type.SINGLE,
            error_message="""
                Joke can only be defined in a single joke. All single jokes must
                contain a joke.
            """
        )


    @staticmethod
    def _check_value_should_exist_for_type(value: str, values: dict, type: Type, error_message: str) -> str:
        type_as_string: str = values["type"]
        if value and not type_as_string.lower() == type.name.lower():
            raise ValueError(error_message)
        return value


    def as_string(self) -> str:
        return (
            self.joke_by_type.get(self.type, Maybe.empty)
            .value_or(f"Could not find joke with type: '{self.type}'.")
        )


class SubmitJoke(Joke):
    """Class for creating the data necessary to submit a joke."""

    formatVersion: int = 3
    lang: str = "en"
    flags: Flags

    class Config:
        validate_assignment = True


class SubmittedJoke(BaseModel):
    """Class for deserializing the response of a submitted joke."""

    message: str
