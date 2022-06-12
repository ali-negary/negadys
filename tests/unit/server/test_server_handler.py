from unittest import TestCase
from unittest.mock import patch
from io import StringIO


from server.server_handler import Command


class TestCommand(TestCase):
    def setUp(self) -> None:
        # create an instance of command class.
        self.cmh = Command()
        self.cmh.database_contents.update({"test_db": {}})

    def test_set_key_result(self):
        # assign test values.
        self.cmh.in_use_db = "test_db"
        self.cmh.key = "test_key"
        self.cmh.value = "test_value"

        # test
        self.cmh.set_key()
        db_content = self.cmh.database_contents
        self.assertTrue("test_db" in db_content)
        test_db_content = db_content["test_db"]
        self.assertTrue(isinstance(test_db_content["test_key"], str))
        self.assertEqual(test_db_content["test_key"], "test_value")

    def test_set_key_result_replace(self):
        # assign test values.
        self.cmh.database_contents = {"test_db": {"test_key": "dummy_value"}}
        self.cmh.in_use_db = "test_db"
        self.cmh.key = "test_key"
        self.cmh.value = "test_value"

        # test
        self.cmh.set_key()
        db_content = self.cmh.database_contents
        self.assertTrue("test_db" in db_content)
        test_db_content = db_content["test_db"]
        self.assertTrue(isinstance(test_db_content["test_key"], str))
        self.assertEqual(test_db_content["test_key"], "test_value")

    def test_set_key_result_array(self):
        # assign test values.
        self.cmh.in_use_db = "test_db"
        self.cmh.key = "test_key"
        self.cmh.value = '["This", "is", 1, "array"]'

        # test
        self.cmh.set_key()
        db_content = self.cmh.database_contents
        self.assertTrue("test_db" in db_content)
        test_db_content = db_content["test_db"]
        self.assertTrue(isinstance(test_db_content["test_key"], str))
        self.assertEqual(test_db_content["test_key"], '["This", "is", 1, "array"]')

    def test_set_key_success_message(self):
        # assign test values.
        self.cmh.in_use_db = "test_db"
        self.cmh.key = "test_key"
        self.cmh.value = "test_value"

        # test
        expected_message = "> \n"
        with patch("sys.stdout", new=StringIO()) as captured_stdout:
            self.cmh.set_key()
        self.assertEqual(captured_stdout.getvalue(), expected_message)

    def test_get_key_found(self):
        # assign test values.
        self.cmh.database_contents = {"test_db": {"test_key": "dummy_value"}}
        self.cmh.in_use_db = "test_db"
        self.cmh.key = "test_key"

        # test
        expected_message = ">  dummy_value\n"
        with patch("sys.stdout", new=StringIO()) as captured_stdout:
            self.cmh.get_key()
        self.assertEqual(captured_stdout.getvalue(), expected_message)

    def test_get_key_not_found(self):
        # assign test values.
        self.cmh.database_contents = {"test_db": {"test_key": "dummy_value"}}
        self.cmh.in_use_db = "test_db"
        self.cmh.key = "unknown_key"

        # test
        expected_message = f"> Key {self.cmh.key} does not exist in test_db!\n"
        with patch("sys.stdout", new=StringIO()) as captured_stdout:
            self.cmh.get_key()
        self.assertEqual(captured_stdout.getvalue(), expected_message)

    def test_del_key_delete(self):
        # assign test values.
        self.cmh.database_contents = {"test_db": {"test_key": "dummy_value"}}
        self.cmh.in_use_db = "test_db"
        self.cmh.key = "test_key"

        # test
        expected_message = "> \n"
        with patch("sys.stdout", new=StringIO()) as captured_stdout:
            self.cmh.delete_key()
        self.assertEqual(captured_stdout.getvalue(), expected_message)

    def test_del_key_not_found(self):
        # assign test values.
        self.cmh.database_contents = {"test_db": {"test_key": "dummy_value"}}
        self.cmh.in_use_db = "test_db"
        self.cmh.key = "unknown_key"

        # test
        expected_message = f"> Key {self.cmh.key} does not exist in test_db!\n"
        with patch("sys.stdout", new=StringIO()) as captured_stdout:
            self.cmh.delete_key()
        self.assertEqual(captured_stdout.getvalue(), expected_message)

    def test_get_keys_regex_found(self):
        # assign test values.
        self.cmh.database_contents = {
            "test_db": {"test_key0": None, "test_key1": None, "what_key": None}
        }
        self.cmh.in_use_db = "test_db"
        self.cmh.key = "test.*"

        # test
        expected_message = ">  ['test_key0', 'test_key1']\n"

        with patch("sys.stdout", new=StringIO()) as captured_stdout:
            self.cmh.get_keys_regex()
        self.assertEqual(captured_stdout.getvalue(), expected_message)

    def test_get_keys_regex_not_found(self):
        # assign test values.
        self.cmh.database_contents = {"test_db": {"test_key0": None, "test_key1": None}}
        self.cmh.in_use_db = "test_db"
        self.cmh.key = "what.*"

        # test
        expected_message = (
            f"> No keys match the regex {self.cmh.key} in {self.cmh.in_use_db}!\n"
        )
        with patch("sys.stdout", new=StringIO()) as captured_stdout:
            self.cmh.get_keys_regex()
        self.assertEqual(captured_stdout.getvalue(), expected_message)

    def test_use_database_present(self):
        # assign test values.
        self.cmh.database_contents = {"test_db": {}, "to_be_in_use_db": {}}
        self.cmh.in_use_db = "test_db"
        self.cmh.key = "to_be_in_use_db"

        # test
        self.cmh.use_database()
        db_content = self.cmh.database_contents
        self.assertTrue("to_be_in_use_db" in db_content)
        self.assertEqual(self.cmh.in_use_db, "to_be_in_use_db")

    def test_use_database_new_database(self):
        # assign test values.
        self.cmh.database_contents = {"test_db": {}}
        self.cmh.in_use_db = "test_db"
        self.cmh.key = "new_in_use_db"

        # test
        self.cmh.use_database()
        db_content = self.cmh.database_contents
        self.assertTrue("new_in_use_db" in db_content)
        self.assertTrue(isinstance(db_content["new_in_use_db"], dict))
        self.assertEqual(self.cmh.in_use_db, "new_in_use_db")

    def test_list_databases(self):
        # assign test values.
        self.cmh.database_contents = {"test_db_0": {}, "test_db_1": {}}

        # test
        expected_message = ">  ['test_db_0', 'test_db_1']\n"
        with patch("sys.stdout", new=StringIO()) as captured_stdout:
            self.cmh.list_databases()
        self.assertEqual(captured_stdout.getvalue(), expected_message)
