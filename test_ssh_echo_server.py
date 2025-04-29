import pytest
import asyncio
import asyncssh
from ssh_echo_server import start_echo_server

@pytest.mark.asyncio
async def test_echo_server_echoes_input():
    session_info = []

    # Tracker function to collect session data
    def track_session(info):
        session_info.append(info)

    # Start echo server
    port = 8022
    server = await start_echo_server(port=port, session_tracker=track_session)

    try:
        # Connect to server
        async with asyncssh.connect('localhost', port=port,
                                    username='test', password='test',
                                    known_hosts=None) as conn:
            result = await conn.run('echo hello', check=True)
            assert result.stdout.strip() == 'hello'

        # Wait briefly for tracker callback to complete
        await asyncio.sleep(0.1)

        # Check tracker captured session info
        assert len(session_info) == 1
        info = session_info[0]
        assert info['username'] == 'test'
        assert info['ip'] in ('127.0.0.1', '::1')  # IPv4 or IPv6
        assert info['bytes_received'] > 0
        assert info['duration_sec'] >= 0
    finally:
        server.close()
        await server.wait_closed()

@pytest.mark.asyncio
async def test_server_starts_and_closes():
    server = await start_echo_server(port=8122)
    assert server is not None
    server.close()
    await server.wait_closed()
