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


class Frame(Bitfield.Bitfield):
    """
    A frame that contains a message and the error detecting and correcting of FT8
    """

    def __init__(self):
        super().__init__(Bitfield.frm_len)
        ###################################################
        # Builds a Crc function for Frame
        ###################################################
        configuration = crc.Configuration(
            width=14,
            polynomial=0x6757,
            init_value=0x00,
            final_xor_value=0x00,
            reverse_input=False,
            reverse_output=False,
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
            self.ldpc_n, self.ldpc_d_v, self.ldpc_d_c, systematic=True, sparse=True
        )
        self.ldpc_k = self.ldpc_G.shape[1]
        self.ldpc_v = np.random.randint(2, size=self.ldpc_k)
        self.ldpc_y = pyldpc.encode(self.ldpc_G, self.ldpc_v, self.ldpc_snr)
        self.ldpc_d = pyldpc.decode(self.ldpc_H, self.ldpc_y, self.ldpc_snr)
        self.ldpc_x = pyldpc.get_message(self.ldpc_G, self.ldpc_d)

        self.frame = OrderedDict()
        self.frame["status"] = "init"

    def get_info(self):
        self.frame["msg"] = hex(self.get_bitfield(Bitfield.msg_field))
        self.frame["crc"] = hex(self.get_bitfield(Bitfield.crc_field))
        self.frame["ecc"] = hex(self.get_bitfield(Bitfield.ecc_field))
        return self.frame

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        self.get_info()
        ans = f'Frame: {self.hex()}, status: {self.frame["status"]}, '
        ans += f'Msg: {self.frame["msg"]}, crc: {self.frame["crc"]}, '
        ans += f'Ecc: {self.frame["ecc"]}'
        return ans

    def encode_msg(self, msg):
        """
        Encodes message by creating CRC and LDPC results
        :param msg:
        :return:
        """
        self.frame["status"] = "encoded"
        self.get_info()

        msg0 = None
        msg_bitfield = None
        if isinstance(msg, Bitfield.Bitfield):
            msg0 = msg.get_bitfield()
            msg_bitfield = msg
        elif isinstance(msg, int):
            msg0 = msg
            msg_bitfield = Bitfield.Bitfield(Bitfield.msg_length)
            msg_bitfield.set_value(msg0)

        self.set_bitfield_dynamic(msg0, length=77)

        tmp = msg_bitfield.reverse().get_byte_array()
        crc = self.crc_calculator.checksum(tmp)
        self.set_bitfield_dynamic(crc, length=14)

        msg_crc_int = self.get_bitfield(Bitfield.msg_crc_field)
        msg_crc = Bitfield.Bitfield(Bitfield.msg_crc_length)
        msg_crc.set_value(msg_crc_int)
        msg_crc_rev = msg_crc.reverse()
        msg_crc = msg_crc_rev.get_bit_array()
        ecc = pyldpc.encode(self.ldpc_G, msg_crc, self.ldpc_snr)
        ecc = pyldpc.decode(self.ldpc_H, ecc, self.ldpc_snr)

        ecc_rev = reversed(ecc)
        self.set_bit_array(ecc_rev)

    def decode_bitfield(self, encoded_val):
        """
        Tries to decode frame from bitfield
        :param bitfield:
        :return:
        """
        self.frame["status"] = "decoded"

        self.set_value(encoded_val)
        tmp = self.get_bit_array()
        msg_crc = pyldpc.get_message(self.ldpc_G, tmp)

        msg_crc_bitfield = Bitfield.Bitfield(Bitfield.msg_crc_length)
        msg_crc_bitfield.set_bit_array(msg_crc)
        msg_bits = msg_crc_bitfield.get_bit_array(Bitfield.msg_field)
        crc_value = msg_crc_bitfield.get_bitfield(Bitfield.crc_field)

        crc_expected = self.crc_calculator.checksum(msg_bits)
        if crc_value != crc_expected:
            print(f"Error encounter during decoding bitfield {self}")
            self.frame["status"] = "decoded with errors"
