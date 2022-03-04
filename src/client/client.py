from multiprocessing.connection import Client

import click
from src import SECRET_KEY

LANGUAGES = ["ro", "it", "en", "de"]


@click.command()
@click.option(
    "--file",
    "-f",
    type=str,
    required=True,
    help="path to input filename to be translated",
)
@click.option(
    "--language",
    "-l",
    type=click.Choice(LANGUAGES),
    required=True,
    help='output language, can be one of "en", "it", "ro" or "de"',
)
def main(file, language):
    """A command to translate all lines from specified file to desired language"""
    client = Client(("localhost", 16000), authkey=bytes(SECRET_KEY, "utf-8"))
    with open(file, "r") as f:
        message = {"lines": f.read().splitlines(), "dest_lang": language}
    client.send(message)
    click.echo("Translating, please wait…")
    for line in client.recv():
        click.echo(line)


if __name__ == "__main__":
    main()
