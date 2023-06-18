###############################################################################
# Frame.py
###############################################################################
# This makes the frame that contains the message, error check and error
# correcting codes.
#
# This is cover on section 2 of protocol
###############################################################################
from collections import OrderedDict
import numpy as np
import pyldpc
import crc

import Bitfield
import Msg


class Frame(object):
    """
    A frame that contains a message and the error detecting and correcting of FT8
    """
    def __init__(self, Msg):

        ###################################################
        # Builds a Crc function for Frame
        ###################################################
        configuration = crc.Configuration(
            width=14,
            polynomial=0x6757,
            init_value=0x00,
            final_xor_value=0x00,
            reverse_input=False,
            reverse_output=False
        )
        self.crc_calculator = crc.Calculator(configuration)

        ###################################################
        # Builds a LDPC function for Frame
        ###################################################
        self.ldpc_n = 174
        self.ldpc_d_v = 41
        self.ldpc_d_c = 58
        self.ldpc_snr = 20
        self.ldpc_H, self.ldpc_G = pyldpc.make_ldpc(
            self.ldpc_n,
            self.ldpc_d_v,
            self.ldpc_d_c,
            systematic=True,
            sparse=True)
        self.ldpc_k = self.ldpc_G.shape[1]
        # self.ldpc_v = np.random.randint(2, size=self.ldpc_k)
        # self.ldpc_y = pyldpc.encode(self.ldpc_G, self.ldpc_v, self.ldpc_snr)
        # self.ldpc_d = pyldpc.decode(self.ldpc_H, self.ldpc_y, self.ldpc_snr)
        # self.ldpc_x = pyldpc.get_message(self.ldpc_G, self.ldpc_d)


        self.bitfield = Bitfield(174)
        self.frame = OrderedDict()
        self.frame['status'] = ''

    def encode_msg(self, msg):
        """
        Encodes message by creating CRC and LDPC results
        :param msg:
        :return:
        """
        self.frame['status'] = 'encoded'

        self.frame['msg'] = msg
        self.bitfield.set_bitfield(msg, length=77)

        crc = self.crc_calculator.checksum(msg)
        self.frame['crc'] = crc
        self.bitfield.set_bitfield(crc, length=14)

        ldpc = pyldpc.encode(self.ldpc_G, self.bitfield.get_bitfield(), self.ldpc_snr)
        self.frame['crc'] = crc
        self.bitfield.set_bitfield(crc, length=83)

    def decode_bitfield(self, bitfield):
        """
        Tries to decode frame from bitfield
        :param bitfield:
        :return:
        """
        self.frame['status'] = 'decoded no errors'
        self.bitfield = bitfield


        self.ldpc_d = pyldpc.decode(self.ldpc_H, self.bitfield.get_bitfield(), self.ldpc_snr)
        msg_crc = pyldpc.get_message(self.ldpc_G, self.ldpc_d)

        msg_crc_bitfield = Bitfield.Bitfield(msg_crc, bit_length=91)
        msg_bitfield = msg_crc_bitfield.get_bitfield([76, 0])
        crc_bitfield = msg_crc_bitfield.get_bitfield([90, 77])

        crc_expected = self.crc_calculator.checksum(msg_bitfield)
        if crc_bitfield != crc_expected:
            print(f"Error encounter during decoding bitfield {bitfield}")
            self.frame['status'] = 'decoded with errors'
