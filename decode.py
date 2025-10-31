from bakery import assert_equal
from PIL import Image as PIL_Image

def even_or_odd_bit(bit: int) -> str:
    """
    Takes an integer and returns that integer mod 2 as a string.
    Params:
    bit: int -> the integer to check if even or odd.
    Returns:
    str -> bit % 2 as a string. (0 for even, 1 for odd)
    """
    if bit % 2 == 0:
        return '0'
    else:
        return '1'

assert_equal(even_or_odd_bit(22), '0')
assert_equal(even_or_odd_bit(0), '0')
assert_equal(even_or_odd_bit(23), '1')
assert_equal(even_or_odd_bit(53), '1')

def decode_single_char(color_intensities: list[int]) -> str:
    """
    Takes eight color intensities and converts them to
    binary, then to base 2. Then converts the ordinal
    number to a character value and returns that.
    Params:
    color_intensities: list[int] -> list of color intensities
    Returns:
    str: binary representation of those intensities as a string.
    """
    if len(color_intensities) != 8:
        return ""
    binary_char = ""
    for color_intensity in color_intensities:
        binary_char += even_or_odd_bit(color_intensity)
    ord_char = int(binary_char, 2)
    return chr(ord_char)

assert_equal(decode_single_char([]), "")
assert_equal(decode_single_char([32, 23, 22, 44, 23, 5, 24]), "")
assert_equal(decode_single_char([32, 23, 22, 44, 23, 5, 25, 32]), "N")
assert_equal(decode_single_char([32, 23, 22, 44, 23, 5, 24, 32]), "L")

def decode_chars(color_intensities: list[int], num_chars: int) -> str:
    """
    Takes a list of color intensities and a number of characters.
    Decodes the characters from the color intensitites and
    returns them as one string.
    Params:
    color_intensities: list[int] -> list of RGB color intensity values.
    num_chars: int -> number of chars to decode form the list
    Returns:
    str -> The decoded string.
    """
    if len(color_intensities) != 8*num_chars:
        return None

    decoded_chars = ""
    # takes each group of eight bits and adds their
    # resulting character to the return string.
    for i in range(num_chars):
        decoded_chars += decode_single_char(color_intensities[i*8:i*8+8])
    return decoded_chars

assert_equal(decode_chars(
                 [2, 1, 2, 2, 1, 2, 2, 2, 4, 3, 3, 4, 3, 4, 4, 3]
                 ,2), "Hi")
assert_equal(decode_chars(
                 [2, 1, 2, 2, 2, 2, 2, 1]
                 ,1), "A")
assert_equal(decode_chars([1, 2, 3, 4, 5, 6, 7, 8], 2), None)

def get_message_length(color_intensities: list[int], num_digits: int) -> int:
    """
    Returns the number of characters to expect in the following
    color intensities based on the header of the data with
    a defined number of digits.
    Params:
    color_intensities: list[int] -> color intensity list
    num_digits: int -> num of digits to read
    Returns:
    int -> Num of characters to decode.
    """
    if len(color_intensities) != num_digits*8:
        return 0
    return int(decode_chars(color_intensities[:num_digits*8], num_digits))

assert_equal(get_message_length([22, 24, 25, 31, 32, 32, 32, 35, 22, 42, 43, 45, 46, 47, 49, 50,
                                 42, 52, 53, 55, 56, 57, 59, 61], 3), 167)

assert_equal(get_message_length([20, 254, 45, 95, 40, 90, 20, 40, 200, 254, 45,
                                 95, 40, 95, 20, 45,220, 250, 45, 95, 48, 95, 24, 44], 3), 54)
assert_equal(get_message_length([22,22,23,23,22,22,23,22,26,26,27,27,26,27,26,27,2,42,43,43,44,44,40,42, 23], 3), 0)

def get_encoded_message(color_intensities: list[int]) -> str:
    """
    Decodes the message from a list of
    color intensities.
    Params:
    color_intensities -> list of color intensities to decode
    Returns:
    str -> the decoded message
    """
    message_length = get_message_length(color_intensities[:24], 3)
    return decode_chars(color_intensities[24:message_length*8+24], message_length)

assert_equal(get_encoded_message([254, 254, 255, 255, 254, 254, 254, 254,
                                  254, 254, 255, 255, 254, 254, 254, 254,
                                  254, 254, 255, 255, 254, 254, 255, 254,
                                  254, 255, 254, 254, 255, 254, 254, 254,
                                  254, 255, 255, 254, 255, 254, 254, 255,
                                  254, 254, 254, 254, 254, 254, 254, 254,
                                  254, 254, 254, 254, 254, 254, 254, 254,
                                  254, 254, 254, 254, 254, 254, 254, 254,
                                  254, 254, 254, 254, 254, 254, 254, 254,
                                  254, 254, 254, 254, 254, 254, 254, 254,
                                  252]), "Hi" )
assert_equal(get_encoded_message([254, 254, 255, 255, 254, 254, 254, 254,
                                  254, 254, 255, 255, 254, 254, 254, 254,
                                  254, 254, 255, 255, 254, 254, 255, 254,
                                  254, 255, 254, 254, 255, 254, 254, 254,
                                  254, 255, 255, 254, 255, 254, 254, 255,
                                  254, 254, 254, 254, 254, 254, 254, 254,
                                  254, 254, 254, 254, 254, 254, 254, 254,
                                  254, 254, 254, 254, 254, 254, 254, 254,
                                  254, 254, 254, 254, 254, 254, 254, 254,
                                  254, 254, 254, 254, 254, 254, 254, 254,
                                  252, 244, 244, 255, 255, 254, 245, 220]), "Hi" )
def get_color_values(image: PIL_Image, chl_idx: int) -> list[int]:
    width, length = image.size
    channel_vals = []
    for x in range(width):
        for y in range(length):
            pixel = image.getpixel((x, y))
            channel_vals.append(pixel[chl_idx])
    return channel_vals

green_vals = get_color_values(PIL_Image.open("testing/1_hidden_message.png").convert('RGB'), 1)  #use green channel
assert_equal(green_vals[:24], [254, 254, 255, 255, 254, 254, 254, 254, 254, 254, 255, 255, 254, 254, 255, 254, 254, 254, 255, 255, 254, 255, 254, 254])