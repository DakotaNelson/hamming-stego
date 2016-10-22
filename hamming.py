from PIL import Image, ImageFilter
from matplotlib.pyplot import imshow
import numpy as np
import sys
import textwrap

from math import floor

def str_to_bin(string):
    """ take a string and return a list of integers (1 or 0) representing that
        string in ASCII """
    ret = list(string)
    # convert to binary representation
    ret = ['{:07b}'.format(ord(x)) for x in ret]
    # split the binary into
    ret = [[bit for bit in x] for x in ret]
    # flatten it and convert to integers
    ret = [int(bit) for sublist in ret for bit in sublist]
    return ret

def bin_to_str(binary):
    """ take a list of binary (integer ones and zeros) and return its ascii
        string representation """
    output = []
    for i in range(floor(len(binary)/7)):
        start = i * 7
        # this is gross
        char = binary[start:start+7]
        char = '0b' + ''.join([str(c) for c in char])
        output.append(int(char, 2))

    st = ''.join([chr(o) for o in output])
    return str(st)


# hamming (8,4)

def encode(msg):
    """ passed a list of bits (integers, 1 or 0), returns a hamming(8,4)-coded
        list of bits """
    while len(msg) % 4 != 0:
        # pad the message to length
        msg.append(0)

    msg = np.reshape(np.array(msg), (-1, 4))

    # create parity bits using transition matrix
    transition = np.mat('1,0,0,0,0,1,1,1;\
                         0,1,0,0,1,0,1,1;\
                         0,0,1,0,1,1,0,1;\
                         0,0,0,1,1,1,1,0')

    result =  np.dot(msg, transition)

    # mod 2 the matrix multiplication
    return np.mod(result, 2)


def syndrome(msg):
    """ passed a list of hamming(8,4)-encoded bits (integers, 1 or 0),
        returns an error syndrome for that list """

    msg = np.reshape(np.array(msg), (-1, 8)).T

    # syndrome generation matrix
    transition = np.mat('0,1,1,1,1,0,0,0;\
                         1,0,1,1,0,1,0,0;\
                         1,1,0,1,0,0,1,0;\
                         1,1,1,0,0,0,0,1')

    result = np.dot(transition, msg)

    # mod 2 the matrix multiplication
    return np.mod(result, 2)

def correct(msg, syndrome):
    """ passed a syndrome and a message (as received, presumably with some
        errors), will use the syndrome to correct the message as best possible
    """

    # the syndrome for any incorrect bit will match the column of the syndrome
    # generation matrix that corresponds to the incorrect bit; a syndrome of
    # (1, 1, 0, 1) would indicate that the third bit has been flipped, since it
    # corresponds to the third column of the matrix

    # syndrome generation matrix (copy/pasted from above)
    transition = np.mat('0,1,1,1,1,0,0,0;\
                         1,0,1,1,0,1,0,0;\
                         1,1,0,1,0,0,1,0;\
                         1,1,1,0,0,0,0,1')

    for synd in range(syndrome.shape[1]):
        if not np.any(syndrome[:,synd]):
            # all zeros - no error!
            continue

        # otherwise we have an error syndrome
        for col in range(transition.shape[1]):
            # not very pythonic iteration, but we need the index
            if np.array_equal(transition[:,col], syndrome[:,synd]):
                current_val = msg[synd,col]
                new_val = (current_val + 1) % 2
                msg.itemset((synd,col), new_val)

    return msg

def decode(msg):
    r = np.mat('1,0,0,0,0,0,0,0;\
                0,1,0,0,0,0,0,0;\
                0,0,1,0,0,0,0,0;\
                0,0,0,1,0,0,0,0')

    res = np.dot(r, msg.T)

    # convert to a regular python list, which is a pain
    return res.T.reshape((1,-1)).tolist()[0]


###############################################################################
message = 'this is a message we plan to hide'
bin_message = str_to_bin(message)

print("original message:")
print(bin_message)
print("")

# now that we have a message, encode it using the hamming code
encoded = encode(bin_message)

print("encoded to:")
print(encoded)
print("")

# introduce noise (this simulates transmission)
transmitted = encoded
transmitted[0, 2] = 0

print("we transmitted:")
print(bin_to_str(decode(transmitted)))
print("")

# and calculate an error syndrome
syndrome = syndrome(transmitted)

print("which has a syndrome of:")
print(syndrome)
print("")

# use the error syndrome to correct the received message
corrected = correct(transmitted, syndrome)
print("corrected to:")
print(corrected)
print("")

# decode the now-corrected message
decoded = decode(corrected)
# print(bin_message)
print("decoded to:")
print(decoded)
print("")

print("and finally:")
print(bin_to_str(decoded))
print("")
