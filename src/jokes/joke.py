from dataclasses import dataclass
from typing import Any
from jokes.options import Type
from returns.maybe import Maybe, maybe
from click import get_current_context
from click.core import Context


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


    def __repr__(self) -> str:
        return (
            self.type
            .bind(lambda type: self.joke_by_type.get(type, Maybe.empty))
            .value_or(self.error.error())
        )


@dataclass
class JokeError:
    internalError: bool
    message: Maybe[str]
    causedBy: Maybe[list[str]]
    additionalInfo: Maybe[str]
    
    
    @property
    def debug(self) -> bool:
        """
        Gets the debug value from the current
        thread's context if it exists. If neither
        the thread nor the value exist, returns
        False.
        """
        return (
            self.get_context()
            .map(lambda ctx: ctx.obj.get("DEBUG"))
            .value_or(False)
        )


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
        
        get_error = self.get_debug_error if self.debug else self.get_basic_error

        return get_error().value_or("An unexpected error occurred.")
    
    
    @maybe
    def get_context(self) -> Context | None:
        """
        Gets the current thread's context. If no
        context exists, silently fails and returns
        None instead.
        """
        return get_current_context(silent=True)


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