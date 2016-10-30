from PIL import Image, ImageFilter
import numpy as np

def blur(img, blur_radius = 0.1):
    img = Image.fromarray(img)
    blurred = img.copy().filter(ImageFilter.GaussianBlur(radius=blur_radius))
    blurred = np.asarray(blurred)

    return blurred
