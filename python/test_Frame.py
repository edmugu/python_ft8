import unittest
import random

import Bitfield
import Frame

class TestFrame(unittest.TestCase):
    def setUp(self):
        self.frame = Frame.Frame()
        self.msg_bitfield = Bitfield.Bitfield(Bitfield.msg_length)

class TestDecode(TestFrame):
    def test_decode_bitfield_simple_no_error(self):
        random.seed(0)
        self.msg_bitfield.set_patter(mode="REPEAT", val=0xA)
        self.frame.encode_msg(self.msg_bitfield)
        print(self.frame)
        test_frame = Frame.Frame()
        test_frame.decode_bitfield(self.frame.get_bitfield())

        self.assertEquals(self.msg_bitfield, test_frame)
