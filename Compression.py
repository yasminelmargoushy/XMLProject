from queue import PriorityQueue
from JSONConversion_Minifying import PrintMinifiedFile

##########################################################################################
##########################################################################################

# GLOBALS:
HuffmanDict = {}
freqDict = {}
probabilitiesDict = {}
Tree = None

##########################################################################################
##########################################################################################

# CLASSES:


class Node:
    probability = None
    left = None
    right = None
    char = None

    def __init__(self, prob, left, right, char):
        self.probability = prob
        self.left = left
        self.right = right
        self.char = char

    def __lt__(self, other):

        if self.probability < other.probability:
            return True
        else:
            return False

# #########################################################################################
# #########################################################################################

# FUNCTIONS:

# Params:
    # node:Head node of a tree.
    # str: an empty string that would be used in the recursion process to build up the codeword.
def traverse_huff(node, str):
    if node.char is None:
        traverse_huff(node.left, str + '0')
        traverse_huff(node.right, str + '1')
        return
    # print(node.char + " => " + str)
    HuffmanDict[node.char] = str
    return


# Converts a string of bits to an array of bytes
def bitstring_to_bytes(s):
    return int(s, 2).to_bytes((len(s) + 7) // 8, byteorder='big')


# params:
# b: 1 byte integer
# Returns a string of 8 bits
def one_byte_to_bitstring(b):
    temp = bin(b)[2:]
    if len(temp) < 8:
        temp = '0' * (8 - len(temp)) + temp
    return temp

# params:
# byteArr: array of integers each is 1 byte
# Returns a string of bits
def bytes_to_bitstring(byteArr):
    s = ""
    for b in byteArr:
        temp = one_byte_to_bitstring(b)
        s += temp
    return s

##########################################################################################
##########################################################################################

# MAIN:

def PrintCompressedTree():
    inputFile = 'Minified_XML.xml'
    decodedFile = 'decodedTxt.txt'

    # ENCODING FILE
    with open(inputFile, 'rb') as in_file:

        # Read input file as an array of bytes
        fileBytes = in_file.read()

        # Converting the array of bytes to array of integers
        fileByteArr = bytearray(fileBytes)

        # Construct frequencies dictionary
        for key in fileByteArr:
            freqDict[key] = freqDict.get(key, 0) + 1

        # Calculate the sum of frequencies
        total = 0
        for key in freqDict:
            total = total + freqDict[key]

        # Calculate Probability dictionary
        for key in freqDict:
            probabilitiesDict[key] = freqDict[key] / total

        # Construct probabilities priority queue
        q = PriorityQueue()
        for key in probabilitiesDict:
            q.put(Node(probabilitiesDict[key], None, None, key))

        # Construct huffman tree from probabilities queue
        while q.qsize() > 1:
            obj1 = q.get()
            obj2 = q.get()
            newOb = Node((obj1.probability + obj2.probability), obj2, obj1, None)
            q.put(newOb)
        Tree = q.get()

        # Set huffman codes for each symbol(leaf) in the huffman tree.
        traverse_huff(Tree, '')

        # Print Huffman dictionary
        # for key in HuffmanDict:
        #     print(str(key) + " => " + HuffmanDict[key])

        # Constructing the new file's bit-string
        outStr = ""
        for ch in fileByteArr:
            outStr += HuffmanDict[ch]

        # After constructing the new file's bit-string. This string might not be divisible by 8.
        # Since we want the bit string to be a specific number of bytes, so we will add zeros to the last byte.
        # But the number of added zeros has to be known for decoding.
        # So we add one byte at the beginning of the string to indicate the number of redundant bits in the last Byte.

        # Calculating the number of bits of the encoded string before adding redundant bits.
        encodedStringLen = len(outStr)

        # Calculating the number of redundant bits in the last byte.
        redundantBitsNum = one_byte_to_bitstring(8 - (encodedStringLen % 8))

        # Adding redundant bits to the encoded string.
        outStr = redundantBitsNum + outStr + '0' * (8 - (encodedStringLen % 8))

        # Converting the bit string to byte array.
        outByteArr = bitstring_to_bytes(outStr)

        Data = str("Original Length = " + str(len(fileByteArr) * 8))
        Data = Data + "\n"+ str("Encoded Length Without redundant bits = " + str(encodedStringLen))
        Data = Data + "\n"+ str("Encoded Length = " + str(len(outStr)))

        List = []
        List.append(outByteArr)
        List.append(Data)
        List.append(Tree)
        # Writing the bytes to the output file.
        return List

def PrintDecompressedFile(encodedFile, decodedFile, Tree):
    with open(encodedFile, 'rb') as in_file, open(decodedFile, "wb") as out_file:

        # Read encoded file as byte array.
        fileBytes = in_file.read()

        # Convert byte array to array of integers.
        fileByteArr = bytearray(fileBytes)

        # Convert array of integers to bit string.
        in_str = bytes_to_bitstring(fileByteArr)

        # Print the input string of bits.
        # print(in_str)

        # Calculate the number of redundant bits from the first byte of the input string.
        redundantBitsNum = int(in_str[:8], 2)

        # Truncate the first byte of the input string.
        new_str = in_str[8:]

        # Printing the number of redundant bits and the new string after truncating the first byte.
        print("redundant bits number: " + str(redundantBitsNum))
        # print(new_str)

        # Loop through the bits of the input string and traverse huffman tree comparing bits with huffman codes.
        # If a code is completed write it to the output array and set the pointer to the huffman head node.
        # Terminate when you reach the first bit of the redundant bits.
        outArr = []
        curr = Tree
        count = 0
        for ch in new_str:
            # Iterate till the first bit of the redundant bits.
            if count == len(new_str) - redundantBitsNum:
                break
            count += 1
            if curr is None:
                print('Error in encoding')
                exit()
            if ch == '0':
                if curr.left is None:
                    print('Error in encoding')
                    exit()
                else:
                    if curr.left.char is not None:
                        outArr.append(curr.left.char)
                        curr = Tree
                    else:
                        curr = curr.left
            elif ch == '1':
                if curr.right is None:
                    print('Error in encoding')
                    exit()
                else:
                    if curr.right.char is not None:
                        outArr.append(curr.right.char)
                        curr = Tree
                    else:
                        curr = curr.right

        # Write the output array to the output file.
        out_file.write(bytearray(outArr))


def PrintCompressedFile(StringFile):
    String = PrintMinifiedFile(StringFile)
    Minified_file = open('Minified_XML.xml', 'w')
    Minified_file.write(String)
    Minified_file.close()
    EncodedString = PrintCompressedTree()
    return EncodedString

