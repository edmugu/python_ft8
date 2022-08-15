###############################################################################
# Msg.py
###############################################################################
# This makes a message that hashes the call sign and other info.
###############################################################################
from collections import OrderedDict
import copy
import re

class Msg(object):
    type_list = [
        ["free Text", 0b000, 0b000, "n3", "f71"],
        ["DXpedition", 0b000, 0b001, "n3", "c28a", "c28b", "h10", "r5"],
        ["Field Day 1", 0b000, 0b011, "c28a", "c28b", "R1", "n4", "k3", "S7"],
        ["Field Day 2", 0b000, 0b100, "c28a", "c28b", "R1", "n4", "k3", "S7"],
        ["Telemetry", 0b000, 0b101, "t71"],
        ["Std Msg", 0b001, "c28a", "r1a", "c28b", "r1b", "R1", "g15"],
        ["EU VHF 1", 0b010, "c28a", "p1a", "c28b", "p2b", "R1", "g15"],
        ["RTTY RU", 0b011, "t1", "c28a", "c28b", "R1", "r3", "s13"],
        ["NonStd Call", 0b100, "h12", "c58", "h1", "r2", "c1"],
        ["EU VHF 2", 0b101, "h12", "h22", "R1", "r3", "s11", "g25"]
    ]

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

    def raw_message_encode(self, data):
        """
        Package the message in a 77-bit message

        :param data:     orderedDict
        :return:
        """
        start_field = 2
        self._set_bit_field(data["type"], 3)
        possible_type = list(filter(lambda x: x[1] == data["type"], self.type_list))
        if data["type"] == 0b000:
            start_field = 3
            self._set_bit_field(data["subtype"], 3)
            possible_type = list(filter(lambda x: x[2] == data["subtype"], possible_type))

        possible_type = possible_type[0]
        for i in range(start_field, len(possible_type)):
            num = re.findall(r'\d+', possible_type[i])
            num = int(num[0])
            self._set_bit_field(data[possible_type[i]], num)

    def raw_message_decode(self, msg):
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







