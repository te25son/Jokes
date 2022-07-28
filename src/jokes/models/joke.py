from jokes.options import Type
from jokes.models.flags import Flags
from pydantic import root_validator, BaseModel
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
            Type.SINGLE.name.casefold(): Maybe.from_optional(self.joke),
            Type.TWOPART.name.casefold(): Maybe.do(
                "\n".join([s, d])
                for s in Maybe.from_optional(self.setup)
                for d in Maybe.from_optional(self.delivery)
            )
        }


    @root_validator(pre=True)
    def check_valid_joke(cls, values: dict) -> dict:
        """Validates that the incoming joke data is valid."""

        type: str = values["type"].casefold()
        setup, delivery, joke = values.get("setup"), values.get("delivery"), values.get("joke")

        if type == Type.TWOPART.name.casefold():
            assert setup is not None, "Setup field must be included in a twopart joke."
            assert delivery is not None, "Delivery field must be included in a twopart joke."
            assert joke is None, "Joke field cannot be included in a twopart joke."

        elif type == Type.SINGLE.name.casefold():
            assert setup is None, "Setup field cannot be included in a twopart joke."
            assert delivery is None, "Delivery field cannot be included in a twopart joke."
            assert joke is not None, "Joke field must be included in a twopart joke."

        else:
            raise ValueError(f"Unknown joke type: {type}.")

        return values


    def as_string(self) -> str:
        return (
            self.joke_by_type.get(self.type.casefold(), Maybe.empty)
            .value_or(f"Could not find joke with type: '{self.type}'.")
        )


class SubmitJoke(Joke):
    """Class for creating the data necessary to submit a joke."""

    formatVersion: int = 3
    lang: str = "en"
    flags: Flags


class SubmittedJoke(BaseModel):
    """Class for deserializing the response of a submitted joke."""

    message: str
