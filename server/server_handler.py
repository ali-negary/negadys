"""This file contains the server side of In-memory key-value database."""

import re
import sys

from server.config import dumps_directory


class Command:
    """This class contains the commands that the server can process."""

    def __init__(self):
        self.command_type = None
        self.key = None
        self.value = None
        self.database_contents = {"default_db": {}}
        self.in_use_db = "default_db"

    def pre_process_command(self, command):
        """This method gets a variable-length argument and splits it into
        command_type, key, and value."""
        command = command.split(" ")
        self.command_type = command[0]
        # 1: list, exit
        # 2: get, del, keys, use
        # 3: set, load, dump
        if self.command_type == "exit":
            print("exiting...")
            sys.exit(0)

        elif self.command_type == "list":
            self.key = None
            self.value = None

        elif self.command_type in ["get", "del", "keys", "use"]:
            self.key = command[1]
            self.value = None

        elif self.command_type in ["load", "dump"]:
            self.key = command[1]
            self.value = command[2]

        elif self.command_type == "set":
            self.key = command[1]
            # value can be a list/array or a string with spaces
            self.value = " ".join(command[2:])

        else:
            print("Could not recognize command! Please try again.")

    def set_key(self):
        """adds a new key-value to the in-use database or
        update value of the key if exists.
        self.key: key to be added or updated in the in-use database.
        self.value: value."""
        self.database_contents[self.in_use_db][self.key] = self.value
        print("> ")

    def get_key(self):
        """This method gets the value of the key in the in-use database.
        self.key: key to be retrieved from in-use database."""
        if self.key in self.database_contents[self.in_use_db]:
            print("> ", self.database_contents[self.in_use_db][self.key])
        else:
            print(f"> Key {self.key} does not exist in {self.in_use_db}!")

    def delete_key(self):
        """This method deletes the key from the in-use database.
        self.key: key to be deleted from in-use database."""
        if self.key in self.database_contents[self.in_use_db]:
            del self.database_contents[self.in_use_db][self.key]
            print("> ")
        else:
            print(f"> Key {self.key} does not exist in {self.in_use_db}!")

    def get_keys_regex(self):
        """This method gets the keys that match the regex.
        self.key: regular expression to filter the keys in the in-use database."""
        try:
            regex_expression = re.compile(self.key)
            # list keys of the in-use database
            keys = list(self.database_contents[self.in_use_db].keys())
            # get the keys that match the regex_expression
            filtered_list = list(filter(regex_expression.match, keys))
            if len(filtered_list) == 0:
                print(f"> No keys match the regex {self.key} in {self.in_use_db}!")
            else:
                print("> ", filtered_list)
        except re.error:
            print(f"> Invalid regex {self.key}!")

    def use_database(self):
        """This method sets the in-use database. If the database does not exist,
        it will create a new one and sets it as in-use.
        self.key: name of the database to be set as in-use."""
        if self.key in self.database_contents:
            self.in_use_db = self.key
        else:
            self.database_contents[self.key] = {}
            self.in_use_db = self.key
        print("> ")

    def list_databases(self):
        """This method lists all the databases."""
        print("> ", list(self.database_contents.keys()))

    def dump_database(self):
        """This method dumps the database to a file in the path.
        self.key: name of the database to be dumped.
        self.value: path to the directory where the database will be dumped."""
        try:
            if self.key in self.database_contents:
                if self.value is None:
                    self.value = dumps_directory + self.key
                with open(f"{self.value}", "w") as file:
                    for key, value in self.database_contents[self.key].items():
                        file.write(f"{key}, {value}\n")
                file.close()
                print("> ")
            else:
                print(f"> Database {self.key} does not exist!")
        except FileNotFoundError:
            print(f"> Directory {self.value} does not exist!")

    def load_database(self):
        """This method loads the database from a file in the path.
        self.key: path to the directory where the database is located.
        self.value: name of the database to be loaded."""
        try:
            new_database_contents = {}
            with open(f"{self.key}", "r") as file:
                for line in file:
                    line_items = line.rstrip().split(", ")
                    key = line_items[0]
                    value = line_items[1:]
                    # check whether the value is of list/array type.
                    if "[" in "".join(value):
                        value = ", ".join(value)
                    else:
                        value = " ".join(value)
                    new_database_contents[key] = value
            file.close()
            self.database_contents[self.value] = new_database_contents
            print("> ")
        except FileNotFoundError:
            print(f"> File {self.value} does not exist!")

    def run(self, incoming_command):
        """This method runs the command."""
        self.pre_process_command(incoming_command)
        if self.command_type == "set":
            self.set_key()
        elif self.command_type == "get":
            self.get_key()
        elif self.command_type == "del":
            self.delete_key()
        elif self.command_type == "keys":
            self.get_keys_regex()
        elif self.command_type == "use":
            self.use_database()
        elif self.command_type == "list":
            self.list_databases()
        elif self.command_type == "dump":
            self.dump_database()
        elif self.command_type == "load":
            self.load_database()
