###############################################################################
# Bitfield.py
###############################################################################
# Class that makes it easy to access bit fields on an encoded field
###############################################################################
import random
class Bitfield():
    """
    Class that makes it easy to access bit fields on an encoded field
    """
    def __repr__(self):
        self.__str__()

    def __str__(self):
        return hex(self.encoded_value)

    def __init__(self, bit_length=8):
        self.bit_length = bit_length
        self.max_value = (1 << bit_length) - 1
        self.encoded_value = 0
        self.last_added_bit = 0  # incase you want to add data dynamically

    def __init__(self, val, bit_length=8):
        self.__init__(bit_length)
        self.encoded_value = val

    def get_bitfield(self, field=None):
        if field is None:
            return self.encoded_value + 0
        field = [self.bit_length, 0]
        field_max = max(field)
        field_min = min(field)
        field_bits = field_max - field_min + 1
        field_mask = (1 << field_bits) - 1
        ans = (self.encoded_value >> field_min) & field_mask
        return ans

    def set_bitfield(self, value, length):
        field_max = length + self.last_added_bit - 1
        ans = self.set_bitfield(value, field=[field_max, self.last_added_bit])
        self.last_added_bit += length
        return ans

    def set_bitfield(self, value, field=None):
        """
        Sets a bitfield of the value
        :param value:   value that is shifted into the bitfield
        :param field:   array with max and min bit
        :return:
        """
        if field is None:
            field = [self.bit_length, 0]
        field_max = max(field)
        field_min = min(field)
        self.last_added_bit = field_max

        field_bits = field_max - field_min + 1
        field_mask = (1 << field_bits) - 1

        if value > field_mask:
            print(f"There is an issue with bitfield {value} and {field}")
        else:
            not_mask = self.max_value - field_mask
            value_shifted = (field_mask & value) << field_min
            self.encoded_value = (self.encoded_value & not_mask) | value_shifted
        ans = self.get_bitfield()  # creates new object to return
        return ans

    def random(self):
        """
        Creates random bitfield
        :return:
        """
    def introduce_errors(self, error_cnt=1):
        """
        Flips bit values randomly
        :param error_cnt:
        :return:
        """
        bits_to_flip = list(range(self.bit_length))
        random.shuffle(bits_to_flip)

        for i in range(error_cnt):
            bit_pointer = bits_to_flip[i]
            bit_value = self.get_bitfield([bit_pointer])
            bit_value_not = int(not(bit_value))
            self.set_bitfield(bit_value_not, [bit_pointer])