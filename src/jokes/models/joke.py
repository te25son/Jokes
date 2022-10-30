from typing import Callable, TypeVar

from pydantic import BaseModel, Extra, fields, validator

from jokes.models.flags import Flags
from jokes.options import Category, Type, as_list

T1 = TypeVar("T1", bound=BaseModel)
T2 = TypeVar("T2", bound=BaseModel)


field_error: Callable[
    [str, str], str
] = lambda value, field: f"{value} is not a valid {field}."


class JokeBase(BaseModel):
    """Class representing the base fields for all jokes."""

    type: str
    category: str

    @validator("type", "category", pre=True)
    def to_upper(cls, value: str) -> str:
        """Converts incoming field values to uppercase."""

        return value.upper()

    @validator("type")
    def check_type_exists(cls, value: str, field: fields.ModelField) -> str:
        """Check that the type field contains a valid type."""

        assert value in as_list(Type), field_error(value, field.name)
        return value

    @validator("category")
    def check_category_exists(cls, value: str, field: fields.ModelField) -> str:
        """Check that the category field contains a valid category."""

        assert value in as_list(Category), field_error(value, field.name)
        return value

    def match_type(
        self, single_action: Callable[[dict], T1], twopart_action: Callable[[dict], T2]
    ) -> T1 | T2:
        """
        Matches the current type to possible values and calls the given function
        with the data initially passed to this class.
        """

        data = self.dict()

        match Type[self.type]:
            case Type.SINGLE:
                return single_action(data)
            case Type.TWOPART:
                return twopart_action(data)
            case _:
                raise ValueError("Invalid type.")

    class Config:
        extra = (
            Extra.allow
        )  # Allows extra fields in the class. Necessary for the match_type function.


class JokeSingle(BaseModel):
    """Class representing the fields necessary for a single type joke."""

    joke: str

    def __str__(self) -> str:
        return self.joke


class JokeTwopart(BaseModel):
    """Class representing the fields necessary for a twopart type joke."""

    setup: str
    delivery: str

    def __str__(self) -> str:
        return "\n".join([self.setup, self.delivery])


class JokeSubmit(JokeBase):
    """Class representing the fields necessary for submitting a joke to Joke API."""

    formatVersion: int = 3
    lang: str = "en"
    flags: Flags


class JokeSingleSubmit(JokeSubmit, JokeSingle):
    """Class representing the fields necessary for submitting a single type joke to Joke API."""

    pass


class JokeTwopartSubmit(JokeSubmit, JokeTwopart):
    """Class representing the fields necessary for submitting a twopart type joke to Joke API."""

    pass


class JokeSubmitted(BaseModel):
    """Class representing the fields present in the response of a successfully submitted joke."""

    message: str

    def __str__(self) -> str:
        return self.message
