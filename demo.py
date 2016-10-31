from PIL import Image
import numpy as np

from blur import blur, randomize
from hamming import str_to_bin, bin_to_str, encode, decode, syndrome, correct
from stego import insert, extract

# encode our original message using hamming(8,4)
original_message = "we're going to hide this message in an image!"
original_message_bin = str_to_bin(original_message)

print("Input:")
print(original_message)

encoded_message = encode(original_message_bin)

# open up the image we want to use and get it ready to put data in
img = Image.open("image.bmp")
img = np.asarray(img)

# insert our message into the image, then blur the image to simulate
# compression/transmission/general data loss
img_with_message = insert(img, encoded_message)

im = Image.fromarray(img_with_message)
im.save("image_steg.bmp")

blur_the_image = True # change this to not blur the image
if blur_the_image:
    blurred_img = randomize(img_with_message)
else:
    blurred_img = img_with_message

im = Image.fromarray(blurred_img)
im.save("image_blurred.bmp")

# extract the message (with errors) from the message, find out what the errors
# are thanks to hamming, and generate an error syndrome (basically an array
# that says "here's where the errors are")
extracted_msg = extract(blurred_img)
decoded = decode(extracted_msg)
decoded_str = bin_to_str(decoded)

print("")
print("Decoded string:")
print(decoded_str)
print("")

syndrome = syndrome(extracted_msg)

print("")
print("Syndrome:")
print(syndrome.T[:100])
print("")

# using the syndrome, correct the errors in the message, then decode the
# corrected version and convert it to a string
corrected = correct(extracted_msg, syndrome)
final_msg = decode(corrected)
final_msg_string = bin_to_str(final_msg)

# and we're done!
print("")
print("Output:")
print(final_msg_string)
