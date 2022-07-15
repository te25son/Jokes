from typing import Any
from jokes.options import Type


class Joke:
    def __init__(self, data: dict[str, Any]) -> None:
        self.type = data.get("type", "")
        self.error = data.get("error", False)
        self.joke = data.get("joke", "")
        self.setup = data.get("setup", "")
        self.delivery = data.get("delivery", "")
        self.category = data.get("category", "")

    def __repr__(self) -> str:
        if self.type == Type.SINGLE.name.lower():
            return self.joke
        if self.type == Type.TWOPART.name.lower():
            return "\n".join([self.setup, self.delivery])
        return f"No type matched the given type: {self.type}"
