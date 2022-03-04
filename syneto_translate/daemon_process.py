#!/usr/bin/python
from multiprocessing.connection import Listener
from threading import get_native_id, Thread
from typing import Dict, List
import concurrent.futures
import itertools
from syneto_translate.translate import translate_text

import daemon
import logging

import lockfile

PIDFILE = 'dm.pid'
LOGFILE = 'dm.log'

# Configure logging
# logging.basicConfig(level=logging.DEBUG)


def translate(text: str, dest_lang: str) -> str:
    logging.debug(f"Line '{text}' is translated on process {get_native_id()}")
    return translate_text(text, dest_lang)


def process_message(message: Dict) -> List:
    with concurrent.futures.ProcessPoolExecutor() as executor:
        translated_lines = executor.map(translate,
                                        message['lines'],
                                        itertools.repeat(message['dest_lang'], len(message['lines']))
                                        )
        return list(translated_lines)


def handle_client(c):
    msg = c.recv()
    logging.debug(f"Message {msg} received on thread {get_native_id()}")
    translated_msg = process_message(msg)
    c.send(translated_msg)


def echo_server(address, authkey):
    server_c = Listener(address, authkey=authkey)
    logging.debug("Listener ready")
    while True:
        client_c = server_c.accept()
        logging.debug("A new connection accepted...")
        t = Thread(target=handle_client, args=(client_c,))
        t.daemon = True
        t.start()


def start_daemon():
    context = daemon.DaemonContext(pidfile=lockfile.FileLock('dm.pid'), umask=0o002)
    with context:
        echo_server(("", 16000), b"secret-key")


if __name__ == "__main__":
    start_daemon()
