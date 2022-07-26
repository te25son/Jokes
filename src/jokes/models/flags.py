from pydantic import BaseModel


class Flags(BaseModel):
    nsfw: bool = False
    religious: bool = False
    political: bool = False
    racist: bool = False
    sexist: bool = False
    explicit: bool = False
