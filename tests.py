"""
Unit tests for the micro compiler.
"""

import unittest
import os
from compiler import aux_routines
from compiler import sem_routines

# we mock our ExprRec and OpRec class here
class Record(object):
    pass

class TestAuxRoutines(unittest.TestCase):

    def setUp(self):
        self.symbol_table = []
        self.output_file = "output/op_code"

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


class TestSemRoutines(unittest.TestCase):

    def setUp(self):
        self.symbol_table = []
        self.output_file = "output/op_code"

    def test_start(self):
        self.symbol_table = ["dirty", "symbol", "table"]

        sem_routines.start(self.symbol_table)

        self.assertFalse("dirty" in self.symbol_table)

    def test_assign(self):
        r1 = Record()
        r2 = Record()
        r3 = Record()
        r1.name = "A"
        r2.name = "Temp&1"
        r3.val = 1011
        t1 = None

        sem_routines.assign(r1, r2)
        sem_routines.assign(r1, r3)

        with open(self.output_file, 'r') as f:
            t1 = f.read()

        os.remove(self.output_file)

        self.assertEqual(t1, "STORE Temp&1, A\nSTORE 1011, A\n")

    def test_read_id(self):
        r1 = Record()
        r1.name = "A"
        t1 = None

        sem_routines.read_id(r1)

        with open(self.output_file, 'r') as f:
            t1 = f.read()
        os.remove(self.output_file)

        self.assertEqual(t1, "READ A, Integer\n")

    def test_write_expr(self):
        r1 = Record()
        r1.name = "A"
        t1 = None

        sem_routines.write_expr(r1)

        with open(self.output_file, 'r') as f:
            t1 = f.read()
        os.remove(self.output_file)

        self.assertEqual(t1, "WRITE A, Integer\n")

    def test_get_infix(self):
        r1 = Record()
        r2 = Record()
        r3 = Record()
        o1 = Record()
        r1.val = 314
        r2.name = "A"
        r3.name = "BB"
        o1.op = "+"
        t1 = None

        sem_routines.get_infix(r1, o1, r2, self.symbol_table)
        sem_routines.get_infix(r3, o1, r2, self.symbol_table)

        with open(self.output_file, 'r') as f:
            t1 = f.read()
        os.remove(self.output_file)

        self.assertEqual(t1, "DECLARE Temp&3, Integer\nADD 314, A, Temp&3\nDECLARE Temp&4, Integer\nADD BB, A, Temp&4\n")

    def test_process_id(self):
        r1 = Record()
        t1 = None

        sem_routines.process_id(r1, self.symbol_table)

        with open(self.output_file, 'r') as f:
            t1 = f.read()
        os.remove(self.output_file)
        self.assertEqual(t1, "DECLARE A, Integer\n")
        self.assertEqual(r1.name, "A")

    def test_proc_literal(self):
        r1 = Record()

        sem_routines.proc_literal(r1)

        self.assertEqual(r1.val, 1011)

    def test_process_op(self):
        r1 = Record()

        sem_routines.process_op(r1)

        self.assertEqual(r1.op, "+")

    def test_finish(self):
        sem_routines.finish()

        with open(self.output_file, 'r') as f:
            t1 = f.read()
        os.remove(self.output_file)

        self.assertEqual(t1, "HALT")

if __name__ == '__main__':
    unittest.main()
