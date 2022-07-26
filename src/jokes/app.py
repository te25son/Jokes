import click

from jokes.options import Type, Flag, Category, OptionData, as_list
from jokes.requests.get import get_joke
from jokes.requests.submit import submit_joke, SubmitJokeData
from returns.unsafe import unsafe_perform_io
from returns.functions import raise_exception
from returns.io import IOResultE, IO
from click.core import Context


@click.group()
@click.option(
    "--debug/--no-debug", "debug",
    default=False
)
@click.pass_context
def jokes(ctx: Context, debug: bool):
    ctx.ensure_object(dict)
    ctx.obj["DEBUG"] = debug


@jokes.command()
@click.option(
    "-c", "--category", "category",
    type=click.Choice(as_list(Category), case_sensitive=False),
    default=Category.ANY.name
)
@click.option(
    "-t", "--type", "type",
    type=click.Choice(as_list(Type), case_sensitive=False),
    default=Type.SINGLE.name
)
@click.option(
    "-f", "--flag", "flags",
    multiple=True,
    type=click.Choice(as_list(Flag), case_sensitive=False),
    help="""
        Can be used several times to blacklist any flags you do not want to see in your jokes.\n
        E.g. 'jokes -f nsfw -f explicit' will not show any nsfw or explicit jokes.
    """,
    default=[]
)
@click.pass_context
def get(ctx: Context, category: str, type: str, flags: list[str]) -> None:
    joke = get_joke(OptionData(category, type, flags))

    click.echo(unsafe_perform_io(unwrap(ctx, joke)))


# Turned off for now since the api is not allowing submissions at the moment
# @jokes.command()
@click.option(
    "-c", "--category", "category",
    type=click.Choice(as_list(Category)[1:], case_sensitive=False),
    required=True
)
@click.option(
    "-t", "--type", "type",
    type=click.Choice(as_list(Type), case_sensitive=False),
    required=True
)
@click.option(
    "-f", "--flag", "flags",
    multiple=True,
    type=click.Choice(as_list(Flag), case_sensitive=False),
    help="""
        Can be used several times to mark any flags that may pertain to your joke.\n
        E.g. 'jokes -f nsfw -f explicit' tells the API that the joke is nsfw and explicit.
    """,
    default=[]
)
@click.pass_context
def submit(ctx: Context, category: str, type: str, flags: list[str]) -> None:
    flags_as_dict = {f.lower(): True for f in flags}

    # Use SubmitJokeData instead of SubmitJoke to delay validation.
    # We don't want validation errors to appear on the screen immediately
    # or without debug.
    joke = SubmitJokeData(
        type=type,
        category=category,
        flags=flags_as_dict
    )

    if type == Type.TWOPART.name:
        joke.setup = click.prompt("Joke setup", type=str)
        joke.delivery = click.prompt("Joke delivery", type=str)

    elif type == Type.SINGLE.name:
        joke.joke = click.prompt("Joke", type=str)

    click.echo(unsafe_perform_io(unwrap(ctx, submit_joke(joke))))


def unwrap(ctx: Context, result: IOResultE) -> IO:
    if ctx.obj.get("DEBUG", False):
        return result.alt(raise_exception).unwrap()
    else:
        return result.value_or("An unexpected error occurred.")
