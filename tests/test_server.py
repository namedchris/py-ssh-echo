import pytest
import asyncio
import asyncssh
from ssh_echo_server.server import start_echo_server

@pytest.mark.asyncio
async def test_echo_server_echoes_input():

    port = 8022
    server = await start_echo_server(port=port)

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


@pytest.mark.asyncio
async def test_server_starts_and_closes():
    server = await start_echo_server(port=8122)
    assert server is not None
    server.close()
    await server.wait_closed()
