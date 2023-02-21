import unittest
import sys

sys.path.append("..")

import lib.utilities


#
# assertEqual(a,b)	a==b
# assertNotEqual(a,b)	a != b
# assertTrue(x)	bool(x) is True
# assertFalse(x)	bool(x) is False
# assertIs(a,b)	a is b
# assertIs(a,b)	a is b
# assertIsNot(a, b)	a is not b
# assertIsNone(x)	x is None
# assertIsNotNone(x)	x is not None
# assertIn(a, b)	a in b
# assertNotIn(a, b)	a not in b
# assertIsInstance(a, b)	isinstance(a, b)
# assertNotIsInstance(a, b)	not isinstance(a, b)
#

class Testing(unittest.TestCase):

    def test_time_labels(self):
        print(lib.utilities.consolefilledline(left='', pattern='-', right='', width=120))
        self.assertEqual(" " + "-"*118 + " ", lib.utilities.consolefilledline(left='', pattern='-', right='', width=120))


if __name__ == '__main__':
    unittest.main()
