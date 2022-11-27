INTERNAL_JOKE_API_ERROR = "An internal JokeAPI error occurred."
INVALID_RESPONSE = "Improperly configured response."
SINGLE_JOKE_ERROR = (
    "Type 'single' must only contain the field 'joke'. "
    "Cannot contain the fields 'setup' or 'delivery'."
)
TWOPART_JOKE_ERROR = (
    "Type 'twopart' must contain both 'setup' and 'delivery'."
    "Cannot contain the the field 'joke'."
)
UNEXPECTED_ERROR = "An unexpected error occurred."
UNKNOWN_JOKE_TYPE_ERROR = "Unknown joke type '{type}'."
