from PIL import Image
import numpy as np

from blur import blur
from hamming import str_to_bin, bin_to_str, encode, decode, syndrome, correct
from stego import insert, extract

# encode our original message using hamming(8,4)
original_message = str_to_bin("we're going to hide this message in an image!")
encoded_message = encode(original_message)

# open up the image we want to use and get it ready to put data in
img = Image.open("image.bmp")
img = np.asarray(img)

# insert our message into the image, then blur the image to simulate
# compression/transmission/general data loss
img_with_message = insert(img, encoded_message)
print(encoded_message)
blurred_img = img_with_message
#blurred_img = blur(img_with_message)

# extract the message (with errors) from the message, find out what the errors
# are thanks to hamming, and generate an error syndrome (basically an array
# that says "here's where the errors are")
extracted_msg = extract(blurred_img)
decoded = decode(extracted_msg)
syndrome = syndrome(decoded)

# using the syndrome, correct the errors in the message, then decode the
# corrected version and convert it to a string
corrected = correct(extracted_msg, syndrome)
final_msg = decode(corrected)
final_msg_string = bin_to_str(final_msg)

# and we're done!
print(final_msg_string)
