from pydantic import BaseModel
from click import get_current_context
from click.core import Context


class Error(BaseModel):
    internalError: bool
    message: str
    causedBy: list[str]
    additionalInfo: str


    @property
    def debug(self) -> bool:
        """
        Gets the 'Debug' value from the current
        thread's context if it exists. If neither
        the thread nor the value exist, returns
        False.
        """
        return context.obj.get("DEBUG") if (context := self.get_context()) else False


    def get_context(self) -> Context | None:
        """
        Gets the current thread's context. If no
        context exists, silently fails and returns
        None instead.
        """
        return get_current_context(silent=True)


    def __str__(self) -> str:
        """Returns a string representation of the error class."""

        if self.internalError:
            return "An internal JokeAPI error occurred."

        if self.debug:
            return "\n".join([self.message, *self.causedBy, self.additionalInfo])

        return "\n".join(self.causedBy)
