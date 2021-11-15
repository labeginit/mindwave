import unittest
from Command import Command


class TestCommand(unittest.TestCase):
    def test_update_command(self):
        self.assertEqual(Command().update_command(5), "{'_id':'Livingroom TV', 'channel':'6'}")

    def test_process_data(self):
        self.assertEqual(Command().process_data('{"blinkStrength": 255}'), True)
