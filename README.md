# py-ssh-echo

A simple **AsyncSSH-based echo SSH server** designed for testing purposes. This server will echo any input sent over SSH, and track basic session information (e.g., username, IP, bytes received, session duration).

---

## Features

- **Echoes input**: Whatever you send to the server is echoed back.
- **Tracks session metadata**: Collects details like username, IP address, bytes received, and session duration.
- **Easy to use**: Can be run as a standalone server or imported as a module in other Python projects.
- **Customizable**: Choose the port for the server, and track session details through a callback function.

---

## Installation

You can install this package from PyPI:

```bash
pip install ssh-echo-server
```

Alternatively, you can install it from the source:

```bash
git clone https://github.com/yourusername/ssh-echo-server.git
cd ssh-echo-server
pip install .
```

---

## Usage

### As a standalone server

Run the server from the command line:

```bash
python -m ssh_echo_server.server
```

By default, the server will run on **localhost:2222**. You can specify a custom port by passing it as an argument:

```bash
python -m ssh_echo_server.server 2022
```

### As an imported module

You can also import and run the server from your Python scripts:

```python
from ssh_echo_server import start_echo_server

async def main():
    # Optionally, define a callback to track session data
    def track_session(info):
        print(f"Session ended: {info}")

    # Start the echo server on a custom port
    server = await start_echo_server(port=2022, session_tracker=track_session)

    try:
        await asyncio.sleep(60)  # Keep the server running for 60 seconds
    finally:
        # Gracefully shut down the server
        server.close()
        await server.wait_closed()

import asyncio
asyncio.run(main())
```

---

## Running Tests

This package includes unit tests that ensure the server functions correctly.

### Install the test dependencies:

```bash
pip install -r requirements.txt
```

### Run the tests with pytest:

```bash
pytest
```

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Contributing

1. Fork the repository.
2. Create a new branch.
3. Make your changes.
4. Create a pull request.

---

## Author

Your Name - [you@example.com](mailto:you@example.com)
