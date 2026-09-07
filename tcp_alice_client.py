import socket


# Change these two values if Bob is running on a different computer.
SERVER_IP = "127.0.0.1"
SERVER_PORT = 5001

alice_text = b"Good morning"
bob_text = b"Hello"


def get_reply(tcp_socket):
    """Keep reading until Bob closes his sending side."""
    reply = b""

    while True:
        # Alice uses a small read size to match her receive window setting.
        part = tcp_socket.recv(3)
        if part == b"":
            break
        print("Alice received:", part)
        reply += part

    return reply


def main():
    # AF_INET and SOCK_STREAM mean IPv4 TCP.
    alice_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # A 3-byte receive buffer is used for the flow-control experiment.
    alice_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 3)
    # Do not wait for Nagle's algorithm to combine small messages.
    alice_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

    try:
        alice_socket.connect((SERVER_IP, SERVER_PORT))
        print("Alice connected to Bob")

        alice_socket.sendall(alice_text)
        print("Alice sent:", alice_text)

        # Alice is done sending, but she can still receive Bob's reply.
        alice_socket.shutdown(socket.SHUT_WR)

        reply = get_reply(alice_socket)
        print("Complete reply from Bob:", reply)

        if reply != bob_text:
            print("Unexpected reply from Bob")
    finally:
        alice_socket.close()


if __name__ == "__main__":
    main()
