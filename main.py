"""This file contains the client side of In-memory key-value database."""

from server.server_handler import Command


if __name__ == "__main__":
    db_interface = Command()
    while True:
        new_command = input(">>> ")
        db_interface.run(incoming_command=new_command)
