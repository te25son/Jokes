from .joke import (
    JokeBase,
    JokeSingle,
    JokeTwopart,
    JokeSubmit,
    JokeSingleSubmit,
    JokeTwopartSubmit,
    JokeSubmitted
)
from .error import Error
from .flags import Flags

Joke = JokeSingle | JokeTwopart
JokeE = Joke | Error
SubmitJoke = JokeSingleSubmit | JokeTwopartSubmit
SubmittedJokeE = JokeSubmitted | Error
