from multiprocessing.connection import Client
import click


LANGUAGES = ['ro', 'it', 'en', 'de']


@click.command()
@click.option('--file', '-f', type=str, required=True)
@click.option('--language', '-l', type=click.Choice(LANGUAGES), required=True)
def main(file, language):
    """A command to translate all lines from specified file to desired language"""
    client = Client(("localhost", 16000), authkey=b"secret-key")
    with open(file, 'r') as f:
        message = {"lines": f.read().splitlines(), "dest_lang": language}
    client.send(message)
    for line in client.recv():
        click.echo(line)


if __name__ == '__main__':
    main()
