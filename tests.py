"""
Unit tests for the micro compiler.
"""

import unittest
import os
from compiler import aux_routines

# we mock our ExprRec and OpRec class here
class Record(object):
    pass

class TestAuxRoutines(unittest.TestCase):

    def setUp(self):
        self.symbol_table = []
        self.output_file = "compiled_code/op_code"
        self.record = Record()

    def test_generate(self):
        test3, test4 = None, None

        # First test with generate with 3 args
        aux_routines.generate("DECLARE", "A", "Integer", s4=None, output_file=self.output_file)
        with open(self.output_file, 'r') as f:
            test3 = f.read()

        os.remove(self.output_file)

        # Now test generate with 4 args
        aux_routines.generate("ADD", "314", "A", s4="Temp&1", output_file=self.output_file)
        with open(self.output_file, 'r') as f:
            test4 = f.read()

        os.remove(self.output_file)

        self.assertEqual(test3, "DECLARE A, Integer\n")
        self.assertEqual(test4, "ADD 314, A, Temp&1\n")

    def test_extract(self):
        r1 = Record()
        r2 = Record()
        r1.name = "test"
        r2.val = 1011

        t1 = aux_routines.extract(r1)
        t2 = aux_routines.extract(r2)

        self.assertEqual(t1, "test")
        self.assertEqual(t2, 1011)

    def test_extract_op(self):
        r1 = Record()
        r2 = Record()
        r1.op = "+"
        r2.op = "-"

        t1 = aux_routines.extract_op(r1)
        t2 = aux_routines.extract_op(r2)

        self.assertEqual(t1, "ADD")
        self.assertEqual(t2, "SUB")

    def test_look_up(self):
        self.symbol_table.append("in_table")

        t1 = aux_routines.look_up("in_table", self.symbol_table)
        t2 = aux_routines.look_up("not_in_table", self.symbol_table)

        self.assertEqual(t1, True)
        self.assertEqual(t2, False)

    def test_enter(self):
        aux_routines.enter("in_table", self.symbol_table)
        self.assertTrue("in_table" in self.symbol_table)
        self.assertFalse("not_in_table" in self.symbol_table)

    def test_check_id(self):
        aux_routines.check_id("A", self.symbol_table)
        t1 = None

        self.assertTrue("A" in self.symbol_table)
        with open(self.output_file, 'r') as f:
            t1 = f.read()
        os.remove(self.output_file)
        self.assertEqual(t1, "DECLARE A, Integer\n")

    def test_get_temp(self):
        t1 = aux_routines.get_temp(self.symbol_table)
        t2 = aux_routines.get_temp(self.symbol_table)
        t3 = None

        self.assertEqual(t1, "Temp&1")
        self.assertEqual(t2, "Temp&2")
        self.assertTrue(t1 in self.symbol_table)
        self.assertTrue(t2 in self.symbol_table)

        with open(self.output_file, 'r') as f:
            t3 = f.read()

        os.remove(self.output_file)
        self.assertEqual(t3, "DECLARE Temp&1, Integer\nDECLARE Temp&2, Integer\n")

if __name__ == '__main__':
    unittest.main()
