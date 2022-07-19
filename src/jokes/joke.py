from dataclasses import dataclass
from typing import Any
from jokes.options import Type
from returns.maybe import Maybe


@dataclass
class Joke:
    type: Maybe[str]
    joke: Maybe[str]
    setup: Maybe[str]
    delivery: Maybe[str]
    category: Maybe[str]
    error: "JokeError"


    @property
    def joke_by_type(self) -> dict[str, Maybe[str]]:
        return {
            Type.SINGLE.name.lower(): self.joke,
            Type.TWOPART.name.lower(): Maybe.do(
                "\n".join([s, d])
                for s in self.setup
                for d in self.delivery
            )
        }


    @staticmethod
    def create(data: dict[str, Any]) -> "Joke":
        return Joke(
            type = Maybe.from_optional(data.get("type")),
            joke = Maybe.from_optional(data.get("joke")),
            setup = Maybe.from_optional(data.get("setup")),
            delivery = Maybe.from_optional(data.get("delivery")),
            category = Maybe.from_optional(data.get("category")),
            error = JokeError.create(data)
        )

      
    def get_joke_string(self) -> Maybe[str]:
        """
        Gets the joke based on the type. If there
        is no type, or no type matches, returns `Nothing`.
        """
        return self.type.bind(lambda type: self.joke_by_type.get(type, Maybe.empty))


    def __repr__(self) -> str:
        return self.get_joke_string().value_or(self.error.error())


@dataclass
class JokeError:
    internalError: bool
    message: Maybe[str]
    causedBy: Maybe[list[str]]
    additionalInfo: Maybe[str]


    @staticmethod
    def create(data: dict[str, Any]) -> "JokeError":
        return JokeError(
            internalError = data.get("internalError", False),
            message = Maybe.from_optional(data.get("message")),
            causedBy = Maybe.from_optional(data.get("causedBy")),
            additionalInfo = Maybe.from_optional(data.get("additionalInfo"))
        )


    def error(self) -> str:
        """
        Returns an error message depending on the existing values.
        Internal errors are checked first. If there are no Joke API
        internal errors, it will attempt to combine the errors included
        in the `causedBy` field. If that field is empty, it will try
        the `message` field. And finally, if that field is empty, it
        will display a custom error message.
        """
        if self.internalError:
            return "An internal JokeAPI error occurred"

        return self.get_basic_error().value_or("An unexpected error occurred.")


    def get_basic_error(self) -> Maybe[str]:
        """
        Gets the error when debug is set to false,
        which is the returned `causedBy` message. If
        that message does not exist, returns the base
        `message`. Otherwise returns `Nothing`.
        """
        return (
            self.causedBy
            .map(lambda errors: "\n".join(errors))
            .lash(lambda _: self.message)
        )


    # TODO: Need a way to reach this bit of code.
    def get_debug_error(self) -> Maybe[str]:
        """
        Gets the error when debug is set to true,
        which is a combined version of all fields in
        the json response.
        Otherwise returns `Nothing`.
        """
        return Maybe.do(
            "\n".join([message, *errors, additional])
            for message in self.message
            for errors in self.causedBy
            for additional in self.additionalInfo
        )