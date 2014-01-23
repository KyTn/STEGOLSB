import random


def generateRandomKey(nBits):
    return random.getrandbits(nBits)

def loadKey(k):
    key = list((bin(k)[2:]))
    return key
