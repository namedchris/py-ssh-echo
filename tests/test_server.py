import pytest
import asyncio
import asyncssh
from ssh_echo_server.server import start_echo_server

@pytest.mark.asyncio
async def test_echo_server_echoes_input():
    session_info = []

    def track_session(info):
        session_info.append(info)

    port = 8022
    server = await start_echo_server(port=port, session_tracker=track_session)

    try:
        async with asyncssh.connect('localhost', port=port,
                                    username='test', password='test',
                                    known_hosts=None) as conn:
            async with conn.create_process() as process:
                process.stdin.write("hello\n")
                output = await process.stdout.readline()
                try:
                    assert "hello" in output
                except AssertionError:
                    print("Output did not contain 'hello'. Here is the full output:")
                    print(output)  # This will print the actual output
                    raise  # Re-raise the exception to fail the test

    finally:
        server.close()
        await server.wait_closed()

    assert session_info  # optionally check for tracking


@pytest.mark.asyncio
async def test_server_starts_and_closes():
    server = await start_echo_server(port=8122)
    assert server is not None
    server.close()
    await server.wait_closed()
