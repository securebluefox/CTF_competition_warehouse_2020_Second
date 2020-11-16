import os, time, string, hashlib
from Crypto.Cipher import AES
from Crypto.Util import Counter
from binascii import hexlify, unhexlify
from secret import flag

banner = '''
    __  ____       _    _____            __
   /  |/  (_)___  (_)  / ___/__  _______/ /____  ____ ___
  / /|_/ / / __ \/ /   \__ \/ / / / ___/ __/ _ \/ __ `__ \\
 / /  / / / / / / /   ___/ / /_/ (__  ) /_/  __/ / / / / /
/_/  /_/_/_/ /_/_/   /____/\__, /____/\__/\___/_/ /_/ /_/
                          /____/
'''

class mini_system:
    def __init__(self):
        print(banner)
        self.key = os.urandom(16)
        self.salt = hashlib.sha256(os.urandom(16)).hexdigest()[24:40]
        self.username_charset = string.digits + string.ascii_letters + "_@"

    def __check_username(self, username):
        for _ in username:
            if _ not in self.username_charset:
                return False
        if len(username) > 12 or len(username) == 0 or username == "root@minisys":
            return False
        else:
            return True

    def sign_up(self):
        print("[+] sign up first.")
        self.r = time.localtime(time.time())[5]
        aes = AES.new(self.key, AES.MODE_CTR, counter=Counter.new(128, initial_value=self.r))
        username = input("> ")
        if not self.__check_username(username):
            print("[!] Invalid username!")
            exit(0)
        token = hexlify(aes.encrypt("{}|{}|{}".format(username, self.salt, 0).encode())).decode()
        print("token={}".format(token))

    def sign_in(self):
        print("[+] sign in with your token.")
        token = input("> ")
        try:
            ct = unhexlify(token)
            aes = AES.new(self.key, AES.MODE_CTR, counter=Counter.new(128, initial_value=self.r))
            pt = aes.decrypt(ct).decode("latin-1").split('|')
            assert(len(pt) == 3)
            username, salt, level = pt[0], pt[1], pt[2]
            print("Welcome {}!".format(username))
            if username == 'root@minisys' and salt == self.salt and level == "1":
                print(flag)
                exit(0)
            else:
                print("ㄣ零χDそτЬ_ωаnτs_а_ɡíгξfгíěnd╰☆ぷ")
        except:
            print("[!] Invalid token!")
    
def main():
    minisys = mini_system()
    minisys.sign_up()
    while True:
        minisys.sign_in()

if __name__ == '__main__':
    main()