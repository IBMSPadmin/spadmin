import unittest
import sys

sys.path.append("..")

import lib.humanbytes as humanbytesClass


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
    hbc = humanbytesClass.HumanBytes

    def test_time_labels(self):
        self.assertEqual("-1 s", self.hbc.format(int(-1), unit="TIME_LABELS", precision=0))
        self.assertEqual("0 s", self.hbc.format(int(0), unit="TIME_LABELS", precision=0))
        self.assertEqual("1 s", self.hbc.format(int(1), unit="TIME_LABELS", precision=0))
        self.assertEqual("1 m", self.hbc.format(int(1 * 60), unit="TIME_LABELS", precision=0))
        self.assertEqual("1 H", self.hbc.format(int(1 * 60 * 60), unit="TIME_LABELS", precision=0))
        self.assertEqual("1 d", self.hbc.format(int(1 * 60 * 60 * 24), unit="TIME_LABELS", precision=0))
        self.assertEqual("1 w", self.hbc.format(int(1 * 60 * 60 * 24 * 7), unit="TIME_LABELS", precision=0))
        self.assertEqual("1 Mo", self.hbc.format(int(1 * 60 * 60 * 24 * 7 * 30), unit="TIME_LABELS", precision=0))
        self.assertEqual("1 Y", self.hbc.format(int(1 * 60 * 60 * 24 * 7 * 30 * 12), unit="TIME_LABELS", precision=0))
        self.assertEqual("3 Y", self.hbc.format(int(1 * 60 * 60 * 24 * 7 * 30 * 36), unit="TIME_LABELS", precision=0))

    def test_boolean(self):
        self.assertEqual("-1 B", self.hbc.format(int(-1), unit="BINARY_LABELS", precision=0))
        self.assertEqual("0 B", self.hbc.format(int(0), unit="BINARY_LABELS", precision=0))
        self.assertEqual("1 B", self.hbc.format(int(1), unit="BINARY_LABELS", precision=0))
        self.assertEqual("1 KiB", self.hbc.format(int(1 * 1024), unit="BINARY_LABELS", precision=0))
        self.assertEqual("1 MiB", self.hbc.format(int(1 * 1024 * 1024), unit="BINARY_LABELS", precision=0))
        self.assertEqual("1 GiB", self.hbc.format(int(1 * 1024 * 1024 * 1024), unit="BINARY_LABELS", precision=0))
        self.assertEqual("1 TiB", self.hbc.format(int(1 * 1024 * 1024 * 1024 * 1024), unit="BINARY_LABELS", precision=0))


if __name__ == '__main__':
    unittest.main()
