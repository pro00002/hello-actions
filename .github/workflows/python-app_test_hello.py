import unittest
from hello import greet

class TestHello(unittest.TestCase):
    def test_default(self):
        self.assertEqual(greet(), "Hello, World!")

    def test_custom(self):
        self.assertEqual(greet("GitHub"), "Hello, GitHub!")

if __name__ == "__main__":
    unittest.main()