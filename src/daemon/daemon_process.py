import concurrent.futures
import itertools
import logging
from multiprocessing.connection import Listener
from threading import Thread, get_native_id
from typing import Dict, List

import click
import daemon
import lockfile
from ratemate import RateLimit
from src import SECRET_KEY
from src.utils.translate import translate_text

RATE_LIMIT = None
PIDFILE = "dm.pid"
LOGFILE = "dm.log"

# Configure logging
logging.basicConfig(level=logging.DEBUG, filename="dm.log")


def translate(text: str, dest_lang: str) -> str:
    waited_time = RATE_LIMIT.wait()
    logging.debug(
        f"Line '{text}' is translated on process {get_native_id()} "
        f"after waited {waited_time}s for limiting rates"
    )
    return translate_text(text, dest_lang)


def process_message(message: Dict) -> List:
    with concurrent.futures.ProcessPoolExecutor() as executor:
        translated_lines = executor.map(
            translate,
            message["lines"],
            itertools.repeat(message["dest_lang"], len(message["lines"])),
        )
        return list(translated_lines)


def handle_client(c):
    msg = c.recv()
    logging.debug(f"Message {msg} received on thread {get_native_id()}")
    translated_msg = process_message(msg)
    c.send(translated_msg)


def start_server(address, authkey):
    server_c = Listener(address, authkey=authkey)
    logging.debug("Listener ready")
    while True:
        client_c = server_c.accept()
        logging.debug("A new connection accepted...")
        t = Thread(target=handle_client, args=(client_c,))
        t.daemon = True
        t.start()


@click.command()
@click.option(
    "--per-sec",
    type=int,
    default=10,
    show_default=True,
    help="Limit number of requests per second",
)
@click.option(
    "--debug-no-daemon",
    is_flag=True,
    help="Use this flag if you don't want a daemon process",
)
def init_server(per_sec, debug_no_daemon):
    click.echo(f"Translation daemon started, throttling at {per_sec} queries/second.")
    global RATE_LIMIT
    RATE_LIMIT = RateLimit(max_count=int(per_sec), per=1)
    if debug_no_daemon:
        start_server(("", 16000), bytes(SECRET_KEY, "utf-8"))
    else:
        context = daemon.DaemonContext(pidfile=lockfile.FileLock("dm.pid"), umask=0o002)
        with context:
            start_server(("", 16000), bytes(SECRET_KEY, "utf-8"))


def start_daemon():
    init_server(auto_envvar_prefix="QUERIES")


if __name__ == "__main__":
    start_daemon()
