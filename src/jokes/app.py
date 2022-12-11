import random

import click
from click.core import Context

from jokes.models import GetEndpointParams
from jokes.options import Categories, Flags, Languages, Types
from jokes.requests import get_joke


@click.group()
@click.option("--debug/--no-debug", "debug", default=False)
@click.pass_context
def jokes(ctx: Context, debug: bool):
    ctx.ensure_object(dict)
    ctx.obj["DEBUG"] = debug


@jokes.command()
@click.option(
    "-c",
    "--category",
    "category",
    type=click.Choice([c.value for c in Categories], case_sensitive=False),
    default=Categories.ANY.name,
)
@click.option(
    "-t",
    "--type",
    "type",
    type=click.Choice(type_list := [t.value for t in Types], case_sensitive=False),
    default=random.choice(type_list),
)
@click.option(
    "-f",
    "--flag",
    "flags",
    multiple=True,
    type=click.Choice([f.value for f in Flags], case_sensitive=False),
    help="""
        Can be used several times to blacklist any flags you do not want to see in your jokes.\n
        E.g. 'jokes -f nsfw -f explicit' will not show any nsfw or explicit jokes.
    """,
    default=[],
)
@click.option(
    "-l",
    "--lang",
    "lang",
    type=click.Choice([l.value for l in Languages], case_sensitive=False),
    default=Languages.EN.name,
)
@click.option("--safe/--unsafe", "safe", default=False)
@click.pass_context
def get(ctx: Context, category: str, type: str, flags: tuple[str], lang: str, safe: bool) -> None:
    ctx.obj["SAFE_MODE"] = safe

    params = GetEndpointParams(type=type, category=category, lang=lang, blacklist_flags=list(flags))

    click.echo(get_joke(params))
