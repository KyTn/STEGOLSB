from PIL import ImageChops
from PIL import ImageStat
import math
import time
def getTimeMillis():
    return int(round(time.time() * 1000))

def calcPSNR(image1, image2):
    """ Calculate peak signal-to-noise-ratio of the difference between image1
        and image2 (see http://en.wikipedia.org/wiki/PSNR).  Returns 1,000,000
        (instead of infinity) if the images are identical, otherwise returns
        the PSNR in dB.  The higher the value, the more similar the images.
    """
    diff = ImageChops.difference(image1, image2)
    istat = ImageStat.Stat(diff)
    sqrtMSE = istat.rms[0]
    psnr = 20.0 * math.log10(255.0 / sqrtMSE) if sqrtMSE != 0 else 1000*1000
    return psnr

def printBinFromInt(n):
    aux = str(bin(n))
    aux = aux[2:]
    zeros = 8 - len(aux)
    aux = (zeros*"0")+aux
    print aux[:4]+" "+aux[4:]
    
def getLSB(bits):
    return bits[-1]

def getTwoLSB(bits):
    twoLSB = bits[-2]
    if twoLSB == 'b':
        return '0'
    else:
        return twoLSB
    

def getCircularData(list, index):
    return list[index % len(list)]

def stringTobits(s):
    asciiList =  stringToASCII(s)
    lst = ''
    for c in asciiList:
        bi = bin(c)[2:]
        le = len(bi)
        bii = ((8-le)*"0")+bi
        lst += bii
    return [int(i) for i in str(lst)]
    '''result = []
    for c in s:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        result.extend([int(b) for b in bits])
    return result'''

def bitsToString(b):
    binlist = split_len(b, 8)
    res = []
    for a in binlist:
        res += [BinaryListToInt(a)]
    return ''.join(ASCIIToString(res))

def mergeList(nums):
    return int(''.join(map(str, nums)))

def intToBinaryList(n):
    b = bin(n)
    num = int(b[2:])
    lst = [int(i) for i in str(num)]
    return lst

def BinaryListToInt(bL):
    l =  mergeList(bL)
    l = int(str(l),2)
    return l
    
def split_len(seq, length):
    return [seq[i:i+length] for i in range(0, len(seq), length)]

def stringToASCII(s):
    return [ord(c) for c in s]

def ASCIIToString(s):
    return [chr(c) for c in s]