###############################################################################
# Bitfield.py
###############################################################################
# Class that makes it easy to access bit fields on an encoded field
###############################################################################
import random

msg_len = 77
crc_len = 14
ecc_len = 83
frm_len = 174

msg_field = [msg_len - 1, 0]
crc_field = [msg_len + crc_len - 1, msg_len]
ecc_field = [ecc_len + max(crc_field), max(crc_field) + 1]

msg_crc_length = msg_len + crc_len
msg_crc_field = [max(crc_field), 0]


class Bitfield:
    """
    Class that makes it easy to access bit fields on an encoded field
    """

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"bits: {self.bit_length} value: {hex(self.encoded_value)}"

    def __init__(self, bit_length=8):
        self.bit_length = bit_length
        self.max_value = (1 << bit_length) - 1
        self.encoded_value = 0
        self.reverse_value = 0
        self.last_added_bit = 0  # incase you want to add data dynamically

    def __eq__(self, other):
        if isinstance(other, Bitfield):
            return self.encoded_value == other.encoded_value
        else:
            return False

    def int(self):
        return self.encoded_value

    def hex(self):
        return hex(self.int())

    def set_value(self, value):
        self.encoded_value = value

    def copy(self):
        ans = Bitfield(self.bit_length)
        ans.set_value(self.encoded_value)
        return ans

    def reverse(self):
        ans = 0
        for i in range(self.bit_length):
            tmp = int(bool(self.encoded_value & (1 << i)))
            ans += tmp << (self.bit_length - 1 - i)
        left_over_size = (4 - (self.bit_length % 4)) % 4
        ans = (ans >> left_over_size) & (self.max_value >> left_over_size)
        ans_bitfield = Bitfield(self.bit_length)
        ans_bitfield.set_value(ans)
        return ans_bitfield

    def get_bitfield(self, field=None):
        if field is None:
            return self.encoded_value + 0
        field_max = max(field)
        field_min = min(field)
        field_bits = field_max - field_min + 1
        field_mask = (1 << field_bits) - 1
        ans = (self.encoded_value >> field_min) & field_mask
        return ans

    def set_bitfield_dynamic(self, value, length):
        field_max = length + self.last_added_bit - 1
        ans = self.set_bitfield(value, field=[field_max, self.last_added_bit])
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
        self.last_added_bit = field_max + 1

        field_bits = field_max - field_min + 1
        field_mask = (1 << field_bits) - 1

        if value > field_mask:
            print(f"There is an issue with bitfield {value} and {field}")
        else:
            not_mask = self.max_value - (field_mask << field_min)
            value_shifted = (field_mask & value) << field_min
            self.encoded_value = (self.encoded_value & not_mask) | value_shifted
        ans = self.get_bitfield()  # creates new object to return
        return ans

    def random(self):
        """
        Creates random bitfield
        :return:
        """
        self.encoded_value = random.randint(0, self.max_value)

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
            bit_value_not = int(not (bit_value))
            self.set_bitfield(bit_value_not, [bit_pointer])

    def get_byte_array(self, length=None):
        """
        returns an array of bytes
        :return:
        """
        hex_str = hex(self.encoded_value)
        hex_str = hex_str.replace("0x", "")
        ans = []

        for b in hex_str:
            tmp = int(b, 16)
            ans.append(tmp)
        ans = bytes(ans)
        return ans

    def get_bit_array(self, length=None):
        """
        returns an array of bits
        :return:
        """
        n = self.bit_length
        if length is not None:
            n = length
        val = self.int()

        ans = []
        for i in range(n):
            tmp = int(bool(val & (1 << i)))
            ans.append(tmp)

        return ans

    def set_bit_array(self, bit_array):
        bit_array0 = list(bit_array)
        ans = 0
        for n, b in enumerate(bit_array0):
            ans += int(bool(b)) << n

        self.encoded_value = ans
        return ans

    def set_patter(self, mode="REPEAT", val=0):
        valid_modes = ["FIXED", "REPEAT", "INC", "RANDOM"]
        if mode.upper() not in valid_modes:
            print("issue happen")
        else:
            m = mode.upper()
            if m == "REPEAT":
                val0 = hex(val).replace("0x", "")
                val1 = val0 * int(1 + (self.bit_length / 4))
                val2 = int(val1, 16)
                val3 = val2 & self.max_value
                self.set_value(val3)
