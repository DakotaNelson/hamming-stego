import random

from PIL import Image, ImageFilter
import numpy as np

def blur(img, blur_radius=0.2):
    img = Image.fromarray(img)
    blurred = img.copy().filter(ImageFilter.GaussianBlur(radius=blur_radius))
    blurred = np.asarray(blurred)

    return blurred

def randomize(img, noise_level=.03):
    """ given an array, randomizes the values in that array

        noise_level [0,1] controls the overall likelihood of a bit being
        flipped. This overall level is then multiplied by the levels variable,
        which modifies the noise level for the various significant bit values
        (i.e. it makes it so that less significant bits are more likely to be
        flipped, which is accurate)
    """
    levels = [.005, .01, .05, .10, .15, .25, .35, .45]
    # more or less randomly chosen modifiers for each bit significance level

    for val in np.nditer(img, op_flags=['readwrite']):
        xor_val = 0
        for level in levels:
            if random.random() < level * noise_level:
                xor_val = (xor_val << 1) | 1
            else:
                xor_val = (xor_val << 1) | 0
        #print('{:08b}'.format(int(xor_val)))
        val[...] = val ^ xor_val

    return img
