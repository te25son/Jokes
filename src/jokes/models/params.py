from click import get_current_context
from pydantic import BaseModel, Field, validator


def filter_items(items: list[str | None]) -> set[str]:
    """Filters none values from given list and returns a set."""
    return set(filter(None, items))


class GetEndpointParams(BaseModel):
    """
    Class representing the query parameters to be included in the get endpoint url.
    Fields containing an empty string ("") will be converted to a query parameter with an empty value, i.e. `?param=`.
    Fields of type `None` will be converted to a valueless query parameter, i.e.`?param`.
    """

    type: str
    category: str
    lang: str
    blacklist_flags: str | None = Field(default="", alias="blacklistFlags")
    safe_mode: str | None = Field(default=None, alias="safe-mode")

    @validator("blacklist_flags", pre=True)
    def format_blacklist_flags(cls, value: list[str]) -> str:
        """Joins the incoming blacklist flags into a single string."""

        return "+".join(value)

    def to_filtered_dict(self) -> dict[str, str]:
        """
        Filters out the empty optional values and returns the model as a dictionary.
        """
        safe_mode = context.obj.get("SAFE_MODE") if (context := get_current_context(silent=True)) else False
        included_fields = filter_items(
            [
                "type",
                "lang",
                "blacklist_flags" if self.blacklist_flags else None,
                "safe_mode" if safe_mode else None,
            ]
        )

        return super().dict(by_alias=True, include=included_fields)

    class Config:
        allow_population_by_field_name = True
        validate_assignment = True
