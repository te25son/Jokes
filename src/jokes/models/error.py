from pydantic import BaseModel
from click import get_current_context
from click.core import Context
from returns.maybe import maybe


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
        return (
            self.get_context()
            .map(lambda ctx: ctx.obj.get("DEBUG"))
            .value_or(False)
        )


    @maybe
    def get_context(self) -> Context | None:
        """
        Gets the current thread's context. If no
        context exists, silently fails and returns
        None instead.
        """
        return get_current_context(silent=True)


    def get_basic_error(self) -> str:
        """
        Meant to be the error when 'Debug' is set
        to 'False'.
        Simply formats and returns the 'causedBy' error. 
        """
        return "\n".join(self.causedBy)


    def get_exhaustive_error(self) -> str:
        """
        Meant to be the error when 'Debug' is set
        to 'True'.
        Returns a formatted string of all error types
        present in the response.
        """
        return "\n".join([self.message, *self.causedBy, self.additionalInfo])


    def as_string(self) -> str:
        if self.internalError:
            return "An internal JokeAPI error occurred"

        return self.get_exhaustive_error() if self.debug else self.get_basic_error()

