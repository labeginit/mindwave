import unittest
from Command import Command


class TestCommand(unittest.TestCase):
    def test_update_command(self):
        command = Command()
        command.action = 2
        self.assertEqual(command.update_command(), "{'_id':'Livingroom TV', 'channel':'2'}")

    def test_process_data(self):
        command = Command()
        command.process_data('{"blinkStrength": 255}')
        self.assertEqual(command.blinks, 1)

