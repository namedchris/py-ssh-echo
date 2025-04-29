import asyncssh
import os
import time
from typing import Callable, Optional
import logging
import sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)
logger.propagate = False

DEFAULT_PORT = 2222

logger.info("Starting logging...")

key = asyncssh.generate_private_key('ssh-rsa')

class EchoSSHServer(asyncssh.SSHServer):

    def connection_made(self, conn):
       logger.info(f"New connection from {conn.get_extra_info('peername')}")

    def connection_lost(self, exc):
        logger.info(f"Connection closed: {exc}")

    def password_auth_supported(self):
        return True

    async def validate_password(self, username, password):
        return True

    def session_requested(self):
        return EchoSSHSession()

class EchoSSHSession(asyncssh.SSHServerSession):
    def __init__(self):
        self._input = ''
        self._chan = None
        self._peername = None
        self._buffer = ''

    def connection_made(self, chan):
        self._chan = chan
        self._peername = chan.get_extra_info('peername')

    def connection_lost(self,exc):
        logger.info(f"Connection closed:/n"
                f"ip: {self._peername[0] if self._peername else 'unknown'}/n"
                f"input: {self._input}"
            )

    def shell_requested(self):
        return True  # Accept interactive shell

    def data_received(self, data, datatype):
        self._input += data
        self._buffer += data
        if '\n' in self._buffer:
            lines = self._buffer.split('\n')
            for line in lines[:-1]:
                if self._chan:
                    self._chan.write(f"{line}\n> ")
            self._buffer = lines[-1]

async def start_echo_server(port=DEFAULT_PORT):
    """Start the echo SSH server and return the server object."""
    server = await asyncssh.listen('127.0.0.1', port,
                                   server_factory=lambda: EchoSSHServer(),
                                   server_host_keys=key)
    print(f"SSH Echo Server listening on localhost:{port}")
    logger.info(f"SSH Echo Server listening on localhost:{port}")

    return server