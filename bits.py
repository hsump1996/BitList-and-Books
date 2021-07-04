# Part 1 goes here!

class ChunkError(Exception):

    def __init__(self, message):
        self.message = message

class DecodeError(Exception):

    def __init__(self, message):
        self.message = message

class BitList:

    def __init__(self, bits: str):
        for x in bits:
            if x != '0' and x != '1':
                raise ValueError('Format is invalid; does not consist of only 0 and 1')
        self.bits = bits

    def __str__(self):

        return self.bits

    @staticmethod
    def from_ints(*args):

        for arg in args:
            if arg not in (0, 1):
                raise ValueError('Format is invalid; does not consist of only 0 and 1')

        return BitList(''.join([str(i) for i in args]))

    def __eq__(self, other):

        return self.bits == str(other.bits)

    def arithmetic_shift_left(self):
        newString = ''
        index = 0

        for bit in self.bits:
            if index != 0:
                if index == len(self.bits) - 1:
                    newString += bit
                    newString += '0'
                    break
                else:
                    newString += bit
                    index = index + 1
            else:
                index = index + 1

        self.bits = newString

    def arithmetic_shift_left(self):
        newString = ''
        index = 0

        for bit in self.bits:
            if index != 0:
                if index == len(self.bits) - 1:
                    newString += bit
                    newString += '0'
                    break
                else:
                    newString += bit
                    index = index + 1
            else:
                index = index + 1

        self.bits = newString

    def arithmetic_shift_right(self):
        newString = ''
        index = 0

        for bit in self.bits:
            if index == 0:
                newString += bit
                newString += bit
                index = index + 1
            elif index == len(self.bits) - 1:
                break
            else:
                newString += bit
                index = index + 1

        self.bits = newString

    def bitwise_and(self, other):
        newString = ''
        others_bits = str(other)
        for i, bit in enumerate(self.bits):
            if bit == others_bits[i]:
                newString += bit
            else:
                newString += '0'

        return BitList(newString)

    def chunk(self, chunk_length: int):
        if len(self.bits) % chunk_length != 0:
            raise ChunkError('The bits cannot be divided evenly')

        bit_int_list = [int(bit) for bit in self.bits]
        return [bit_int_list[x:x+chunk_length] for x in range(0, len(bit_int_list), chunk_length)]

    def decode(self, encoding: str = 'utf-8'):
        if encoding == 'utf-8':
            chars = []
            lead_start_i = 0

            while lead_start_i < len(self.bits):
                lead_end_i = lead_start_i + 8
                leading_byte = self.bits[lead_start_i:lead_end_i]

                throw_off_i = leading_byte.find('0')
                if throw_off_i == 0:
                    lead_start_i = lead_end_i
                    chars.append(chr(int(leading_byte, 2)))
                    continue
                elif not (1 <= throw_off_i <= 4) or leading_byte.startswith('10'):
                    raise DecodeError('leading byte in invalid format')

                trailing_payload_num = throw_off_i - 1
                lead_start_i = lead_end_i + (8 * trailing_payload_num)
                continuation_bytes = self.bits[lead_end_i:lead_start_i]
                continuation_byte_list = [continuation_bytes[i*8:(i+1)*8] for i in range(trailing_payload_num)]
                if any([not byte.startswith('10') for byte in continuation_byte_list]):
                    raise DecodeError('continuation byte in invalid format (some byte does not start with 10)')

                codepoint = leading_byte[throw_off_i+1:] + ''.join([byte[2:] for byte in continuation_byte_list])
                chars.append(chr(int(codepoint, 2)))

            return ''.join(chars)
        elif encoding == 'us-ascii':
            return ''.join([chr(int(self.bits[i:i+7], 2)) for i in range(0, len(self.bits), 7)])
        else:
            raise ValueError('invalid encoding')