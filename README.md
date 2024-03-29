```
          _____                   _______                   _____                    _____                    _____
         /\    \                 /::\    \                 /\    \                  /\    \                  /\    \
        /::\    \               /::::\    \               /::\____\                /::\    \                /::\    \
        \:::\    \             /::::::\    \             /:::/    /               /::::\    \              /::::\    \
         \:::\    \           /::::::::\    \           /:::/    /               /::::::\    \            /::::::\    \
          \:::\    \         /:::/~~\:::\    \         /:::/    /               /:::/\:::\    \          /:::/\:::\    \
           \:::\    \       /:::/    \:::\    \       /:::/____/               /:::/__\:::\    \        /:::/__\:::\    \
           /::::\    \     /:::/    / \:::\    \     /::::\    \              /::::\   \:::\    \       \:::\   \:::\    \
  _____   /::::::\    \   /:::/____/   \:::\____\   /::::::\____\________    /::::::\   \:::\    \    ___\:::\   \:::\    \
 /\    \ /:::/\:::\    \ |:::|    |     |:::|    | /:::/\:::::::::::\    \  /:::/\:::\   \:::\    \  /\   \:::\   \:::\    \
/::\    /:::/  \:::\____\|:::|____|     |:::|    |/:::/  |:::::::::::\____\/:::/__\:::\   \:::\____\/::\   \:::\   \:::\____\
/\:::\  /:::/    \::/    / \:::\    \   /:::/    / \::/   |::|~~~|~~~~~     \:::\   \:::\   \::/    /\:::\   \:::\   \::/    /
 \:::\/:::/    / \/____/   \:::\    \ /:::/    /   \/____|::|   |           \:::\   \:::\   \/____/  \:::\   \:::\   \/____/
  \::::::/    /             \:::\    /:::/    /          |::|   |            \:::\   \:::\    \       \:::\   \:::\    \
   \::::/    /               \:::\__/:::/    /           |::|   |             \:::\   \:::\____\       \:::\   \:::\____\
    \::/    /                 \::::::::/    /            |::|   |              \:::\   \::/    /        \:::\  /:::/    /
     \/____/                   \::::::/    /             |::|   |               \:::\   \/____/          \:::\/:::/    /
                                \::::/    /              |::|   |                \:::\    \               \::::::/    /
                                 \::/____/               \::|   |                 \:::\____\               \::::/    /
                                  ~~                      \:|   |                  \::/    /                \::/    /
                                                           \|___|                   \/____/                  \/____/
```

## What is it?

A small CLI app for fetching and displaying jokes on your terminal :clown_face:

Jokes are taken from the [public JokeAPI](https://v2.jokeapi.dev/). A lot of the jokes on there are **VERY** dark and likely to be insulting. It is possible to filter out *some* of the gutter humor (but why tho? gutter humor is the best humor). To filter jokes, see the [flag section](#Flag).

## How to use it

Jokes has three dependencies that will have to be installed prior to running locally.

1. [poetry](https://python-poetry.org/docs/#installation)
2. [pre-commit](https://pre-commit.com/#installation)
3. [just](https://github.com/casey/just#packages)

Once all three have been installed, clone this repo and "cd" your way into the created folder, e.g. `cd jokes`.

To setup the environment run `just setup`, and activate the virtual environment created by poetry with `poetry shell`.

You should now be able to run the `jokes` command. Try it out by running `jokes get`.

## Options (arguments)

There are a few arguments you can use when calling jokes.

### Category

> Example: `jokes get -c Any` or `jokes get --category Any`
>
> Default: Any

The category tag will specify which category your joke will be in. Use `jokes get --help` to see available categories.

### Type

> Example: `jokes get -t Single` or `jokes get --type Single`
>
> Default: Random

Choose the type of joke, either a single oneliner or a two-parter. Use `jokes get --help` to see available types.

### Flag

> Example: `jokes get -f nsfw -f explicit` or `jokes get --flag nsfw`
>
> Default: []

The flag option can be used once, multiple times, or not at all. It is used to try to filter out unwanted jokes. But it isn't an exact science, so don't be surprised if it doesn't filter out everything.

Use `jokes get --help` to see available flags.

### Lang

> Example: `jokes get -l fr` or `jokes get --lang fr`
>
> Default: EN (English)

Choose the language you want your joke to be in. Choice must be in the [ISO 639-1 format](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes). Current supported languages are English, French, Portuguese, Czech, Spanish, and German.

Note that the option does not translate the jokes but filters jokes that have been submitted in the desired language.

### Safe Mode

> Example: `jokes get --safe` or `jokes get --unsafe`
>
> Default: unsafe

If you use the safe option, the API will attempt to filter out any offensive, dark, or insulting jokes. Be warned that some gutter humor may work its way through the filtering, but it's unlikely.

## Coming Soon(ish)

~~The ability to submit a joke to the Joke API with this CLI is currently under construction :hammer_and_wrench:. The code has been written but it hasn't been possible to test since the Joke API has temporarily disabled joke submissions at this time.~~

## Development

### Debug

> Example: `jokes --debug`
>
> Default: Off

Debug is turned off by default but can be turned on using the debug flag.

Errors are typically returned as "An unexpected error occurred." If you wish to see more information about the nature of the error, use the debug flag. This is only intended for development purposes.

### Testing

Tests are written in pytest and can be called using either `just test` while the virtual environemnt is activated.
