from .error import Error
from .flags import Flags
from .joke import (
    JokeBase,
    JokeSingle,
    JokeSingleSubmit,
    JokeSubmit,
    JokeSubmitted,
    JokeTwopart,
    JokeTwopartSubmit,
)
from .response import APIResponse

Joke = JokeSingle | JokeTwopart
JokeE = Joke | Error
SubmitJoke = JokeSingleSubmit | JokeTwopartSubmit
SubmittedJokeE = JokeSubmitted | Error
