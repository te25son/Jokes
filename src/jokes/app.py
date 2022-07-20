import click

from jokes.options import Type, Flag, Category, OptionData, as_list
from jokes.request import get_joke
from returns.unsafe import unsafe_perform_io
from returns.functions import raise_exception
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

    if ctx.obj.get("DEBUG", False):
        result = joke.alt(raise_exception).unwrap()
    else:
        result = joke.value_or("An unexpected error occurred.")

    click.echo(unsafe_perform_io(result))
