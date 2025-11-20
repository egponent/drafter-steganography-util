# libraries
from drafter import *
from bakery import assert_equal
from dataclasses import dataclass
from PIL import Image as PIL_Image

set_site_information(
    author="lukajv@udel.edu",
    description="""A steganography utility which lets you encode
    and decode messages into image files.""",
    sources=["N/A"],
    planning=["plan.pdf"],
    links=["https://github.com/UD-F25-CS1/cs1-website-f25-lukajv"]
)
hide_debug_information()
set_website_title("Your Website Title")
set_website_framed(False)

# Decoding Helper Functions

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
def get_color_values(image: PIL_Image.Image, chl_idx: int) -> list[int]:
    """
    Gets a list of color intensities in a
    given channel in a given image.

    Params:
        image: PIL_Image.Image -> image to scan.
        chl_idx: int -> Color channel to make a list of.
    Returns:
        list[int] -> List of color intensities.
    """
    width, length = image.size
    channel_vals = []
    for x in range(width):
        for y in range(length):
            pixel = image.getpixel((x, y))
            channel_vals.append(pixel[chl_idx])
    return channel_vals

def prepend_header(message: str) -> str:
    """
    Determines the length of a message and returns a 
    string with the length of the message in three digits
    prepended to the original message.
    
    Params:
        message: str -> The message.
    Returns:
        str -> Length of message prepended to the message.
    """
    if len(message) >= 100:
        prefix = ''
    elif len(message) >= 10:
        prefix = '0'
    else:
        prefix = '00'
    return prefix + str(len(message)) + message
    
assert_equal(prepend_header("sdf"), '003sdf')
assert_equal(prepend_header(""), '000')
assert_equal(prepend_header("aaaaaaaaaaaa"), '012' + "a"*12)
assert_equal(prepend_header("a"*101), '101' + "a"*101)

def message_to_binary(message: str) -> str:
    """
    Converts a string to binary.
    
    Params:
        message: str -> the message
    Returns:
        str -> binary representation of the message
    """
    result = ""
    for char in message:
        result += format(ord(char), '08b')
    return result

assert_equal(message_to_binary("Hi"), "0100100001101001")
assert_equal(message_to_binary("058"),"001100000011010100111000")
assert_equal(message_to_binary("00"),"0011000000110000")
assert_equal(message_to_binary(""), "")

def new_color_value(color_intensity: int, bit: str) -> int:
    """
    Makes the evenness of a color intensity
    value match a given bit.
    
    Params:
        color_intensity: int -> Base10 color intensity
        bit: str -> 1 or 0 to determine evenness
        
    Returns:
        int -> Base10 color intensity matching
        bit evenness.
    """
    if bit == '1' and color_intensity % 2 == 0:
        return color_intensity + 1
    elif bit == '0' and color_intensity % 2 == 1:
        return color_intensity - 1
    else: return color_intensity

assert_equal(new_color_value(255, '1'), 255)
assert_equal(new_color_value(255, '0'), 254)
assert_equal(new_color_value(254, '1'), 255)
assert_equal(new_color_value(0, '1'), 1)

def hide_bits(image: PIL_Image.Image, bits: str) -> PIL_Image.Image:
    """
    Hides message bits into an image.
    
    Params:
        image: PIL_Image -> The image to encode a message in.
        bits: str -> string of bits to encode
    
    Returns
        PIL_Image -> The encoded message in an image file.
    """
    image_size = image.size
    
    for x in range(image_size[0]):
        for y in range(image_size[1]):
            curr_bit_idx = x*image_size[1] + y
            if curr_bit_idx < len(bits):
                red, green, blue = image.getpixel((x, y))
                green = new_color_value(green, bits[curr_bit_idx])
                image.putpixel((x, y), (red, green, blue))
            else:
                return image
    return image

@dataclass
class State:
    image: PIL_Image.Image
    message: str
    message_bits: str
    color_values: list[int]

@route
def index(state: State) -> Page:
    """ Use FileUpload to allow user to select only png files """
    return Page(state, [
        "Would you like to encode or decode?",
        Button("Encode", "encode_menu"),
        Button("Decode", "decode_menu")
    ])

@route
def decode_menu(state: State) -> Page:
    """"""
    return Page(state, [
        "Select the image you'd like to decode. (PNG only)",
        FileUpload("new_image", accept="image/png"),
        Button("Decode", "decode_image")
    ])

@route
def decode_image(state: State, new_image: PIL_Image.Image) -> Page:
    state.image = new_image
    state.color_values = get_color_values(state.image, 1)
    state.message = get_encoded_message(state.color_values)
    return Page(state, [
        "Your hidden message was:",
        state.message,
        Button("Back", "index")

    ])

@route
def encode_menu(state: State,) -> Page:
    return Page(state, [
        "Select the image that you'd like to use.",
        FileUpload("raw_image"),
        "Enter the message that you'd like to encode.",
        TextArea("user_message"),
        Button("Encode", "encode_image")
    ])

@route
def encode_image(state: State, raw_image: PIL_Image.Image, user_message: str) -> Page:
    rgb_image = raw_image.convert("RGB")
    state.message_bits = message_to_binary(prepend_header(user_message))
    state.image = hide_bits(rgb_image, state.message_bits)
    return Page(state, [
        "Your encoded image!",
        Image(state.image),
        "Would you like to save the image?",
        Download("Download", "encoded_image.png", state.image, "image/png"),
        Button("Back", "index")
    ])


start_server(State(None, "", "", []))
