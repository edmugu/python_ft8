###############################################################################
# Msg.py
###############################################################################
# This makes a message that hashes the call sign and other info.
###############################################################################
from collections import OrderedDict
import copy

class Msg(object):
    def __init__(self):
        msg_enc = 0     # encoded message
        msg_pnt = 77    # message pointer

    def _get_bit_field(self, length):
        """
        Returns the left most bit field pointed by msg_pnt
        :param length:
        :return:
        """
        self.msg_pnt -= length
        bit_field = (2**length - 1) << self.msg_pnt
        ans = bit_field & self.msg_enc
        ans = ans >> self.msg_pnt
        return ans

    def _set_bit_field(self, data, length):
        """
        This will set the leftmost [or MSB] of the message
        :param data:    data to fill
        :param length:  length of the bit field
        :return:        None
        """
        self.msg_pnt -= length
        if self.msg_pnt < 0:
            raise ValueError('message overflow')
        max_value = 2**length - 1
        if not((max_value >= data) and (data >= 0)):
            raise ValueError('Bad bit length')
        self.msg_enc = self.msg_enc | (data << self.msg_pnt)

    def message_encode(self, data):
        """
        Package the message in a 77-bit message

        :param data:     orderedDict
        :return:
        """
        self._set_bit_field(data["type"], 3)

        if data["type"] == 0b000:
            self._set_bit_field(data["subtype"], 3)

            if data["subtype"] == 0b000:
                # Free text
                self._set_bit_field(data["f71"], 71)

            elif data["subtype"] == 0b001:
                # DXpedition
                self._set_bit_field(data["c28a"], 28)
                self._set_bit_field(data["c28b"], 28)
                self._set_bit_field(data["h10"], 10)
                self._set_bit_field(data["r5"], 5)

            elif (data["subtype"] == 0b010) or (data["subtype"] == 0b011):
                # field day
                self._set_bit_field(data["c28a"], 28)
                self._set_bit_field(data["c28b"], 28)
                self._set_bit_field(data["r1"], 1)
                self._set_bit_field(data["n4"], 4)
                self._set_bit_field(data["k3"], 3)
                self._set_bit_field(data["s7"], 7)

            elif data["subtype"] == 0b001:
                # Telemetry
                self._set_bit_field(data["t71"], 71)

        elif data["type"] == 0b001:
            # std data
            self._set_bit_field(data["c28a"], 28)
            self._set_bit_field(data["r1a"], 1)
            self._set_bit_field(data["c28b"], 28)
            self._set_bit_field(data["r1b"], 1)
            self._set_bit_field(data["r1c"], 1)
            self._set_bit_field(data["g15"], 15)

        elif data["type"] == 0b010:
            # EU VHF
            self._set_bit_field(data["c28a"], 28)
            self._set_bit_field(data["p1a"], 1)
            self._set_bit_field(data["c28b"], 28)
            self._set_bit_field(data["p1b"], 1)
            self._set_bit_field(data["r1"], 1)
            self._set_bit_field(data["g15"], 15)

        elif data["type"] == 0b011:
            # RTTY RU
            self._set_bit_field(data["t1"], 1)
            self._set_bit_field(data["c28a"], 28)
            self._set_bit_field(data["c28a"], 28)
            self._set_bit_field(data["r1"], 1)
            self._set_bit_field(data["r3"], 3)
            self._set_bit_field(data["s13"], 13)

        elif data["type"] == 0b100:
            # nonstd call
            self._set_bit_field(data["h12"], 12)
            self._set_bit_field(data["c58"], 58)
            self._set_bit_field(data["h1"], 1)
            self._set_bit_field(data["r2"], 2)
            self._set_bit_field(data["c1"], 1)

        elif data["type"] == 0b101:
            # nonstd call
            self._set_bit_field(data["h12"], 12)
            self._set_bit_field(data["h22"], 22)
            self._set_bit_field(data["r1"], 1)
            self._set_bit_field(data["r3"], 3)
            self._set_bit_field(data["s11"], 11)
            self._set_bit_field(data["g25"], 25)

    def message_decode(self, msg):
        """
        returns an OrderDict with the data in msg
        :param msg:
        :return:
        """
        msg_pnt = 77
        ans = OrderedDict()

        ans["type"] = self._get_bit_field(3)
        if ans["type"] == 0b000:
            ans["subtype"] = self._get_bit_field(3)
            if ans["subtype"] == 0b000:
                ans["f71"] = self._get_bit_field(71)







