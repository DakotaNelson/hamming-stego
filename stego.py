from PIL import Image, ImageFilter
import numpy as np

from hamming import str_to_bin


def set_bit(val, bitNo, bit):
    """ given a value, which bit in the value to set, and the actual bit
    (0 or 1) to set, return the new value with the proper bit flipped """
    mask = 1 << bitNo
    val &= ~mask
    if bit:
        val |= mask
    return val

def insert(img, msg, bits=[1]):
    """ given an image as a numpy matrix and a message as an array of ones
    and zeros, encode the message into the image steganographically and return
    a numpy array representing the image
    optional:
        bits -> which bits to encode the message into; passing [0] will only
                encode into the least significant bit of the image, while
                passing [0, 1, 2, 3, 4, 5, 6, 7] would return the message as
                a numpy array
    """

    msg = np.array(msg)

    try:
        bits = set(bits) # dedupe
        for bit in bits:
            # make sure the bits the user has told us to encode into
            # actually exist
            assert bit in range(8)
    except:
        raise ValueError("bits must be specified as 0 through 7")

    # note that this assumes no repetition
    storage_space = img.size * len(bits)

    if len(msg) > storage_space:
        raise ValueError(("Message ({msglen} bits) too large to fit in image "
                          "({storage} bits available). Try a different image "
                          "or use more bit significance levels in the current "
                          "image.").format(
                              msglen=len(msg),
                              storage=storage_space
                          )
                        )
    elif len(msg) < storage_space:
        padding = np.zeros((storage_space - len(msg)))
        msg = np.append(msg, padding)

    msgIndex = 0

    img = np.copy(img)

    for val in np.nditer(img, op_flags=['readwrite']):
        # val is either the R, G, or B channel of one pixel
        for bit in bits:
            setTo = msg[msgIndex]
            val[...] = set_bit(int(val), bit, setTo)
            msgIndex += 1

    return img

def extract(img, bits=[1]):
    """ given an image as a numpy matrix, extract steganographically encoded
    data from the image, returning a list of bits (integer 1 or 0) representing
    the message extracted
    optional:
        bits -> which bits to encode the message into; passing [0] will only
                encode into the least significant bit of the image, while
                passing [0, 1, 2, 3, 4, 5, 6, 7] would return the message as
                a numpy array
    """

    try:
        bits = set(bits) # dedupe
        for bit in bits:
            # make sure the bits the user has told us to encode into
            # actually exist
            assert bit in range(8)
    except:
        raise ValueError("bits must be specified as 0 through 7")

    msg = []

    for val in np.nditer(img):
        # val is either the R, G, or B channel of one pixel
        byte = '{:08b}'.format(int(val))
        for bit in bits:
            msg.append(int(byte[-(bit+1)]))

    return np.array(msg).reshape((-1, 8))
