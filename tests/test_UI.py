"""
UI unit test
"""

from chess.UI import *
import unittest

class test_UI(unittest.TestCase):
    def test_init(self):
        pass

    def test_player_input(self):
        u=UI()
        def input(prompt):
            return "a1"
        self.assertEqual(("a1","a1"),u.player_input(input=input))

if __name__ == '__main__':
    unittest.main()