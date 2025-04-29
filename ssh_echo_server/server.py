import asyncssh
import os
import time
from typing import Callable, Optional

HOST_KEY_FILE = 'ssh_host_key'
DEFAULT_PORT = 2222

if not os.path.exists(HOST_KEY_FILE):
    key = asyncssh.generate_private_key('ssh-rsa')
    with open(HOST_KEY_FILE, 'wb') as f:
        f.write(key.export_private_key(format_name='openssh'))

class EchoSSHServer(asyncssh.SSHServer):
    def __init__(self, session_tracker: Optional[Callable] = None):
        self.session_tracker = session_tracker

    def connection_made(self, conn):
        print('Connection from', conn.get_extra_info('peername'))

    def connection_lost(self, exc):
        print(f"Connection closed: {exc}")

    def password_auth_supported(self):
        return True

    async def validate_password(self, username, password):
        return True

    def session_requested(self):
        return EchoSSHSession(self.session_tracker)

class EchoSSHSession(asyncssh.SSHServerSession):
    def __init__(self, tracker):
        self._input = ''
        self._chan = None
        self._peername = None
        self._tracker = tracker
        self._buffer = ''

    def connection_made(self, chan):
        self._chan = chan
        self._peername = chan.get_extra_info('peername')

    def connection_lost(self,exc):
        self._tracker({
            "ip": self._peername[0] if self._peername else 'unknown',
            "input": self._input,
        })

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

async def start_echo_server(port=DEFAULT_PORT, session_tracker: Optional[Callable] = None):
    """Start the echo SSH server and return the server object."""
    server = await asyncssh.listen('127.0.0.1', port,
                                   server_factory=lambda: EchoSSHServer(session_tracker),
                                   server_host_keys=[HOST_KEY_FILE])
    print(f"SSH Echo Server listening on localhost:{port}")

    return server
