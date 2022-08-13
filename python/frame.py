###############################################################################
# frame.py
###############################################################################
# This makes the frame that contains the message, error check and error
# correcting codes.
###############################################################################
from collections import OrderedDict

class frame(object):
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
        self._set_bit_field(msg["subtype"], 3)

        if msg["type"] == 0b000:
            if msg["subtype"] == 0b000:
                # Free text



