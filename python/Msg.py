###############################################################################
# Msg.py
###############################################################################
# This makes the frame that contains the message, error check and error
# correcting codes.
###############################################################################
from collections import OrderedDict

class Msg(object):
    def __init__(self):
        print("Frame created")
        self.reset()

    def reset(self):
        msg_enc = 0     # encoded message
        msg_pnt = 77    # message pointer

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

    def message_encode(self, msg):
        """
        Package the message in a 77-bit message

        :param msg:     orderedDict
        :return:
        """
        self._set_bit_field(msg["type"], 3)

        if msg["type"] == 0b000:
            self._set_bit_field(msg["subtype"], 3)

            if msg["subtype"] == 0b000:
                # Free text
                self._set_bit_field(msg["f71"], 71)

            elif msg["subtype"] == 0b001:
                # DXpedition
                self._set_bit_field(msg["c28a"], 28)
                self._set_bit_field(msg["c28b"], 28)
                self._set_bit_field(msg["h10"], 10)
                self._set_bit_field(msg["r5"], 5)

            elif (msg["subtype"] == 0b010) or (msg["subtype"] == 0b011):
                # field day
                self._set_bit_field(msg["c28a"], 28)
                self._set_bit_field(msg["c28b"], 28)
                self._set_bit_field(msg["r1"], 1)
                self._set_bit_field(msg["n4"], 4)
                self._set_bit_field(msg["k3"], 3)
                self._set_bit_field(msg["s7"], 7)

            elif msg["subtype"] == 0b001:
                # Telemetry
                self._set_bit_field(msg["t71"], 71)

        elif msg["type"] == 0b001:
            # std msg
            self._set_bit_field(msg["c28a"], 28)
            self._set_bit_field(msg["r1a"], 1)
            self._set_bit_field(msg["c28b"], 28)
            self._set_bit_field(msg["r1b"], 1)
            self._set_bit_field(msg["r1c"], 1)
            self._set_bit_field(msg["g15"], 15)

        elif msg["type"] == 0b010:
            # EU VHF
            self._set_bit_field(msg["c28a"], 28)
            self._set_bit_field(msg["p1a"], 1)
            self._set_bit_field(msg["c28b"], 28)
            self._set_bit_field(msg["p1b"], 1)
            self._set_bit_field(msg["r1"], 1)
            self._set_bit_field(msg["g15"], 15)

        elif msg["type"] == 0b011:
            # RTTY RU
            self._set_bit_field(msg["t1"], 1)
            self._set_bit_field(msg["c28a"], 28)
            self._set_bit_field(msg["c28a"], 28)
            self._set_bit_field(msg["r1"], 1)
            self._set_bit_field(msg["r3"], 3)
            self._set_bit_field(msg["s13"], 13)

        elif msg["type"] == 0b100:
            # nonstd call
            self._set_bit_field(msg["h12"], 12)
            self._set_bit_field(msg["c58"], 58)
            self._set_bit_field(msg["h1"], 1)
            self._set_bit_field(msg["r2"], 2)
            self._set_bit_field(msg["c1"], 1)

        elif msg["type"] == 0b101:
            # nonstd call
            self._set_bit_field(msg["h12"], 12)
            self._set_bit_field(msg["h22"], 22)
            self._set_bit_field(msg["r1"], 1)
            self._set_bit_field(msg["r3"], 3)
            self._set_bit_field(msg["s11"], 11)
            self._set_bit_field(msg["g25"], 25)




