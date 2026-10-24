# TCP Client-Server Lab — CSCI 414

A group networking lab demonstrating TCP communication between a Python client (Alice) and server (Bob).

The programs exchange messages over a local TCP connection and explore receive-buffer settings, reading data in small chunks, and closing a connection’s sending side while continuing to receive data.

## Features

- IPv4 TCP communication using Python’s built-in `socket` module.
- Alice sends `Good morning`; Bob sends `Hello`.
- Small receive reads: up to 3 bytes for Alice and 4 bytes for Bob.
- Configurable receive-buffer settings and disabled Nagle’s algorithm.
- TCP half-close using `shutdown(socket.SHUT_WR)`.

## Files

| File | Description |
|---|---|
| `tcp_alice_client.py` | Client that connects to Bob and exchanges messages. |
| `tcp_bob_server.py` | Server that accepts Alice’s connection and exchanges messages. |
| `Lab 02 Group 2.docx` | Group lab report. |
| `captured packages.pdf` | Packet-capture documentation. |

## Requirements

Python 3. No third-party packages are required.

## Run Locally

From the repository folder, start the server:

```bash
python tcp_bob_server.py
```

In a second terminal, start the client:

```bash
python tcp_alice_client.py
```

Both programs use `127.0.0.1` on port `5001` by default. Each prints the received chunks and complete message before closing.

## Notes

TCP is a byte stream, so individual reads do not necessarily match individual sends. The operating system also determines the effective receive-buffer size; requesting a small buffer does not guarantee an equally small TCP receive window.

Completed as a group assignment for CSCI 414 at St. Cloud State University.
