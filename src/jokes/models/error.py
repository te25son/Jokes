from pydantic import BaseModel
from click import get_current_context


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
        return context.obj.get("DEBUG") if (context := get_current_context(silent=True)) else False


    def __str__(self) -> str:
        """Returns a string representation of the error class."""

        if self.internalError:
            return "An internal JokeAPI error occurred."

        if self.debug:
            return "\n".join([self.message, *self.causedBy, self.additionalInfo])

        return "\n".join(self.causedBy)
