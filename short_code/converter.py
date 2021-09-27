"""
Core feature of this solution
Converter could transfer decimal number to string (and string to decimal number)
String represented as number (in other base notation and other alphabet of symbols)

Example:
[ALPHABET] '0123456789ABCDEF'
[BASE] len(ALPHABET) = 16
[NUMBER -> NUMBER_REPRESENTATION_AS_STRING] 11 -> 'B', 16 -> '10'; 30 -> '1E' 
"""

from django.conf import settings


class Converter(object):

    @staticmethod
    def decimal_to_other_base(decimal_number: int):

        alphabet = settings.SORTED_ALPHABET
        base = len(alphabet)
        requested_short_code_length = settings.REQUESTED_SHORT_CODE_LENGTH

        if decimal_number < 0:
            raise ValueError(f'Initial number {decimal_number} is negative')

        digits_string = ''

        remainder = decimal_number
        while remainder:
            digits_string = (alphabet[int(remainder % base)]) + digits_string
            remainder = remainder // base

        difference_in_digits = requested_short_code_length - len(digits_string)
        if difference_in_digits < 0:
            raise ValueError(f'Initial number {decimal_number} is out of range for parameter'
                             f' REQUESTED_SHORT_CODE_LENGTH {requested_short_code_length}')
        elif difference_in_digits > 0:
            pre_string = ''
            for i in range(difference_in_digits):
                pre_string += alphabet[0]
            digits_string = pre_string + digits_string
        return digits_string

    @staticmethod
    def other_base_to_decimal(number_in_other_base: str):

        alphabet = settings.SORTED_ALPHABET
        base = len(alphabet)

        decimal_number = 0

        rank = len(number_in_other_base)
        counter = 0
        for digit_symbol in number_in_other_base:
            digit_index = alphabet.find(digit_symbol)
            if digit_index == -1:
                raise ValueError(f'Unexpected symbol in number {number_in_other_base}')

            counter += 1
            decimal_number += digit_index * (base ** (rank - counter))

        return decimal_number

