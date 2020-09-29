# Define constant properties
SECRET_KEYS = [0, 0, 0, 0, 0]  # DUMMY
NUM_BITS = 12
BLOCK_SIZE_BITS = 48
BLOCK_SIZE = BLOCK_SIZE_BITS / 8
MAX_VALUE = (2 << (NUM_BITS - 1))
BIT_MASK = MAX_VALUE - 1


class Cipher(object):
    def __init__(self, k0, k1, k2, k3, k4):
        self.k0 = k0
        self.k1 = k1
        self.k2 = k2
        self.k3 = k3
        self.k4 = k4

        self._rand_start = 0
        self.sbox0, self.rsbox0 = self.generate_boxes(106)
        self.sbox1, self.rsbox1 = self.generate_boxes(81)

    def my_srand(self, seed):
        self._rand_start = seed

    def my_rand(self):
        if self._rand_start == 0:
            self._rand_start = 123459876
        hi = self._rand_start / 127773
        lo = self._rand_start % 127773
        x = 16807 * lo - 2836 * hi
        if x < 0:
            x += 0x7fffffff
        self._rand_start = (x % (0x7fffffff + 1))
        return self._rand_start

    def generate_boxes(self, seed):
        self.my_srand(seed)
        sbox = range(MAX_VALUE)
        rsbox = range(MAX_VALUE)

        for i in xrange(MAX_VALUE):
            r = self.my_rand() % MAX_VALUE
            temp = sbox[i]
            sbox[i] = sbox[r]
            sbox[r] = temp

        for i in xrange(MAX_VALUE):
            rsbox[sbox[i]] = i

        return sbox, rsbox

    def ror7(self, b):
        return ((((b) & BIT_MASK) >> 7) | (((b) << (NUM_BITS - 7)) & BIT_MASK))

    def rol7(self, b):
        return ((((b) << 7) & BIT_MASK) | (((b) & BIT_MASK) >> (NUM_BITS - 7)))

    def pad_string(self, s):
        num_blocks = len(s) / BLOCK_SIZE
        num_remainder = len(s) % BLOCK_SIZE

        pad = (BLOCK_SIZE - num_remainder) % BLOCK_SIZE
        for i in xrange(BLOCK_SIZE - num_remainder):
            s += chr(pad)
        return s

    def unpad_string(self, s):
        pad = ord(s[-1]) & 0xff
        if pad == 0 or pad > BLOCK_SIZE:
            pad = BLOCK_SIZE
        return s[:-pad]

    def string_to_bits_list(self, s):
        input_chars = s
        num_blocks = len(s) / BLOCK_SIZE

        bits_list = []
        for i in xrange(num_blocks):
            block = 0
            for j in xrange(BLOCK_SIZE):
                block = block << 8
                block = block | ord(input_chars[i * BLOCK_SIZE + j])
            for j in xrange(BLOCK_SIZE_BITS, 0, -NUM_BITS):
                bits_list.append((block >> (j - NUM_BITS)) & BIT_MASK)
        return bits_list

    def bits_list_to_string(self, input_bits):
        num_input_bits_per_block = BLOCK_SIZE_BITS / NUM_BITS;
        output_chars = []
        for i in xrange(0, len(input_bits), num_input_bits_per_block):
            block = 0
            for j in xrange(num_input_bits_per_block):
                block = block << NUM_BITS
                block = block | (input_bits[i+j])
            for j in xrange(BLOCK_SIZE, 0, -1):
                output_chars.append((block >> ((j-1) * 8)) & 0xff)
        return "".join([chr(x) for x in output_chars])

    def encrypt_bits(self, b):
        boxed = self.sbox0[self.sbox1[self.sbox0[(b & BIT_MASK) ^ self.k0] ^ self.k1] ^ self.k2] ^ self.k3
        return (self.ror7(boxed) ^ self.k4) & BIT_MASK;

    def decrypt_bits(self, b):
        unboxed = self.rol7((b & BIT_MASK) ^ self.k4) ^ self.k3
        return (self.rsbox0[self.rsbox1[self.rsbox0[unboxed] ^ self.k2] ^ self.k1] ^ self.k0);

    def encrypt(self, s):
        pad_s = self.pad_string(s)
        bits = self.string_to_bits_list(pad_s)
        return self.bits_list_to_string([(self.encrypt_bits(b)) for b in bits])

    def decrypt(self, s):
        bits = self.string_to_bits_list(s)
        dec = [self.decrypt_bits(b) for b in bits]
        return self.unpad_string(self.bits_list_to_string(dec))


if __name__ == "__main__":
    '''
    DIFFERENTECH Cipher

    As you are monitoring your station, you intercepted a hex-encoded encrypted
    message, along with its plain text.

    plaintext = "Cryptanalysis has coevolved together with cryptography"
    ciphertext = ("2371697013e9bdcb50133102f2c8c08a69b93e1878ac7939ac7049"
                  "8ddd5dee019f4be4ec8dd3a612c8708a1169701d5d3de3169c7b1d"
                  "146146146146").decode('hex')

    You have also previously chanced upon another encrypted message, which you
    will need to decrypt.  Taking a look at the algorithm, and past interceptions,
    you noticed that the 12-bit numbers:
        2684 encrypts to 2568
        3599 encrypts to 3185
    You realize that you just might be able to break it before lunch!

    NOTE: GIVE ONE ENCRYPTED FLAG AS PART OF THE QUESTIION AND Try to decrypt
    '''

    #find the right SECRET_KEYS
    SECRET_KEYS = [0,0,0,0,0]
    cipher = Cipher(*SECRET_KEYS)
    test_text = "Cryptanalysis has coevolved together with cryptography"
    ciphertext = ("2371697013e9bdcb50133102f2c8c08a69b93e1878ac7939ac7049"
                  "8ddd5dee019f4be4ec8dd3a612c8708a1169701d5d3de3169c7b1d"
                  "146146146146").decode('hex')


    
    #enc = cipher.encrypt(test_text)
    dec = cipher.decrypt(ciphertext)

    if test_text == dec:
        print("That's right!")
    else:
        print("Try again!")



