###############################################################################
# frame.py
###############################################################################
# This makes the frame that contains the message, error check and error
# correcting codes.
#
# This is cover on section 2 of protocol
###############################################################################
from collections import OrderedDict
import numpy as np
import pyldpc
import Msg
import crc


class Frame(object):
    """
    A frame that contains a message and the error detecting and correcting of FT8
    """
    def __init__(self):

        ###################################################
        # Builds a Crc function for Frame
        ###################################################
        configuration = crcConfiguration(
            width=14,
            poly=0x6757,
            init_value=0x00,
            final_xor_value=0x00,
            reverse_input=False,
            reverse_output=False
        )
        self.crc_calculator = crc.CrcCalculator(configuration, use_table=False)

        ###################################################
        # Builds a LDPC function for Frame
        ###################################################
        n = 15
        d_v = 4
        d_c = 5
        snr = 100
        H, G = pyldpc.make_ldpc(n, d_v, d_c, systematic=True, sparse=True)
        k = G.shape[1]
        v = np.random.randint(2, size=k)
        y = pyldcp.encode(G, v, snr)
        d = decode(H, y, snr)
        x = get_message(G, d)


        self.frame = OrderedDict()
        self.frame["msg"] = Msg.Msg()
        self.frame["crc"] = 2**14 - 1  # 14-bit crc
        self.frame["ldpc"] = 2**83 - 1 # 83-bit ldpc
        print("Frame created")

    def calculate_crc(self):
        """
        This adds the 14-bit cyclic redundancy check to the frame
        :return:
        """
        data = self.frame["crc"].msg_enc
        self.frame["crc"] = self.crc_calculator.calculate_checksum(data)


