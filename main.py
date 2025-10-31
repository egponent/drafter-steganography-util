# libraries
from drafter import *
from bakery import assert_equal
from dataclasses import dataclass
from PIL import Image as PIL_Image
# local
from decode import get_color_values, get_encoded_message

@dataclass
class State:
    image: PIL_Image
    message: str

@route
def index(state: State) -> Page:
    """ Use FileUpload to allow user to select only png files """
    return Page(state, [
        "Would you like to encode or decode?",
        # Button("Encode", "encode_menu")
        Button("Decode", "decode_menu")
    ])

assert_equal(
    index(State(image=None, message='')),
    Page(state=State(image=None, message=''),
         content=['Would you like to encode or decode?', Button(text='Decode', url='/decode_menu')]))

@route
def decode_menu(state: State) -> Page:
    """"""
    return Page(state, [
        "Select the image you'd like to decode. (PNG only)",
        FileUpload("new_image", accept="image/png"),
        Button("Decode", "decode_image")
    ])

assert_equal(
    decode_menu(State(image=None, message='')),
    Page(state=State(image=None, message=''),
         content=["Select the image you'd like to decode. (PNG only)",
                  FileUpload(name='new_image'),
                  Button(text='Decode', url='/decode_image')]))

@route
def decode_image(state: State, new_image: bytes) -> Page:
    state.image = PIL_Image.open(io.BytesIO(new_image)).convert('RGB')
    state.message = get_encoded_message(get_color_values(state.image, 1))
    return Page(state, [
        "Your hidden message was:",
        state.message,
        Button("Back", "index")

    ])

# idk how to unit test this

start_server(State(None, ""))
