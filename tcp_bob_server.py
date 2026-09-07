import socket


HOST = "127.0.0.1"
PORT = 5001

alice_text = b"Good morning"
bob_text = b"Hello"


def read_from_alice(connection):
    """Read until Alice half-closes her write side."""
    message = b""

    while True:
        # Bob reads in small pieces for the receive-window experiment.
        data = connection.recv(4)
        if data == b"":
            break
        print("Bob received:", data)
        message += data

    return message


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # The server asks for a small 4-byte TCP receive buffer.
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 4)
    server_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

    try:
        server_socket.bind((HOST, PORT))
        server_socket.listen(1)
        print("Bob is waiting for Alice on port", PORT)

        connection, address = server_socket.accept()
        print("Alice connected from", address)

        try:
            # Set these again on the actual client connection.
            connection.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 4)
            connection.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

            # Bob says hello right after the connection is accepted.
            connection.sendall(bob_text)
            print("Bob sent:", bob_text)

            message = read_from_alice(connection)
            print("Complete message from Alice:", message)

            if message != alice_text:
                print("Alice's message was not what was expected")

            # Bob is done sending too, so this sends the final FIN from Bob.
            connection.shutdown(socket.SHUT_WR)
        finally:
            connection.close()
    finally:
        server_socket.close()


if __name__ == "__main__":
    main()
