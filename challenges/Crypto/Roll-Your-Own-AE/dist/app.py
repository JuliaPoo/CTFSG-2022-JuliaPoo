from Crypto.Cipher import AES
from urllib import parse
import base64
import hmac
import re
import os

import secret # Only the server has this >-<

from flask import Flask
from flask import request, make_response, render_template
app = Flask(__name__, template_folder='templates/')

class CryptError(Exception):
    pass
    
class CookieError(Exception):
    pass

class Crypt:
    
    '''
    Encrypt/Decrypt object that totally securely
    implements AES-CBC HMAC-SHA256 yall:
    
    Encrypted message format:
        final_encrypt  = [salt:16][iv:16][encrypted_data]
        encrypted_data = AESCBC(PAD([len:2][data][hmac:32]))
        hmac           = HMACSHA256([len:2][data])
        
    Awesome features of this implementation:
        1. Random IVs!
        2. Salted keys!
        3. Unknown padding! (No padding oracles here!)
    '''
    
    def __init__(self, key:bytes):
        if len(key) != 16:
            raise CryptError("Invalid key size. `key` has to be 16 bytes.")
        self.key = key
    
    @staticmethod
    def _pad(data:bytes)->bytes:
        
        '''
        Pads `data` to blocksize 16 with random
        bytes. No padding oracle attack here >-<
        '''
        
        i = -len(data)%16
        return data+os.urandom(i)
    
    @staticmethod
    def _unpad(data:bytes, length:int)->bytes:
        '''
        Unpads `data`. `length` must be given as
        self._pad pads with random bytes.
        '''
        return data[:length]
    
    def _AESCBC(self, data:bytes, salt:bytes, decrypt=False)->bytes:
        
        '''
        Encrypts/decrypts `data` with self.key
        If `decrypt` == False (default), 
          `data` is encrypted with AES-CBC and 
          the iv appended to the start.
        If `decrypt` == True,
          `data` is decrypted, assuming the iv is
          the first 16 bytes of `data`
        '''
        
        iv = data[:16] if decrypt else os.urandom(16)
        cipher = AES.new(self.key+salt, AES.MODE_CBC, iv=iv)
        if decrypt:
            return cipher.decrypt(data[16:])
        return iv + cipher.encrypt(data)
    
    def _HMAC(self, data:bytes, salt:bytes)->bytes:
        
        '''
        Returns HMAC-SHA256 of `data`
        '''
        
        auth = hmac.new(self.key+salt, digestmod='sha256')
        auth.update(data)
        return auth.digest()
    
    def encrypt(self, data:bytes)->bytes:
        
        '''Encrypts `data`'''
        
        length = len(data)+34
        if not (length < 1<<16):
            raise CryptError("Encryption of `data` length %d>%d not supported"%(length, 1<<16))
        
        # Generate salt
        salt = os.urandom(16)
        
        # Add length field
        data = length.to_bytes(2, 'little') + data
        
        # Generate signature
        hmac = self._HMAC(data, salt)
        data += hmac
        
        # Pad and AES encrypt
        data = self._pad(data)
        data = self._AESCBC(data, salt)
        
        # Add salt to data and return
        return salt+data
    
    def decrypt(self, data:bytes)->bytes:
        
        '''Decrypts data and verifies signature'''

        if len(data)%16 != 0 and len(data)>=80:
            raise CryptError("`data` has to be multiple of 16 and at least length 80")
        
        # Get salt
        salt, data = data[:16], data[16:]
        
        # Verify length field before unpadding
        data = self._AESCBC(data, salt, decrypt=True)
        length = int.from_bytes(data[:2], 'little')
        if not (len(data) < 1<<16 and len(data)-16 < length <= len(data)):
            raise CryptError("`data` has invalid length")
        
        # Unpad data
        data = self._unpad(data, length)
        
        # Verify hmac
        data, hmac = data[:-32], data[-32:]
        if not hmac == self._HMAC(data, salt):
            raise CryptError("`data` does not have a valid signature")
        
        # Remove length field
        data = data[2:]
        return data

class Cookie:

    def __init__(self):
        self.crypt = Crypt(secret.key)
        self.data = None
        pass

    def parse(self, cookie:str)->bool:

        '''
        Parses `cookie`.
            Inits self.cookie, self.data.
        @Returns bool
            True if success
            False if fail. Error can be accessed at self.error
        '''

        self.cookie = cookie
        try:
            cookie = base64.b64decode(cookie+'='*4) # fix padding
        except Exception as e:
            self.error = e
            return False

        try:
            serialized = self.crypt.decrypt(cookie).decode('utf-8', errors='ignore')
        except CryptError as e:
            self.error = e
            return False

        self.data = dict(parse.parse_qsl(serialized, strict_parsing=True))

        return True

    def gen(self, username:str)->bool:

        '''
        Generates cookie based on `username`.
            Inits self.cookie, self.data.
        @Returns bool
            True if success
            False if fail. Error can be accessed at self.error
        '''

        naked_flag = re.findall(r"^CTFSG\{([a-z0-9_]+)\}$", secret.flag)[0]
        self.data = {
            "username": username,
            "flag": naked_flag,
            "placeholder": "yo!~~"
        }
        serialized = parse.urlencode(self.data).encode('utf-8', errors='ignore')

        try:
            cookie = self.crypt.encrypt(serialized)
        except CryptError as e:
            self.error = e
            return False

        self.cookie = base64.b64encode(cookie)
        return True

    def get(self, param:str):

        '''
        Gets `param` from cookie
        @Returns bool
            True if success
            False if fail. Error can be accessed at self.error
        '''

        try:
            if type(self.data) != dict:
                raise CookieError("Cookie not initialised! Call self.gen or self.parse")

            if param not in self.data:
                raise CookieError("Param `%s` not in cookie!"%param)
        except CookieError as e:
            self.error = e
            return False, None

        return True, self.data[param]
        

@app.route('/', methods=['POST', 'GET'])
def index():

    cookie = Cookie()
    status = True
    username = None

    if request.method=='POST' and 'username' in request.form:
        username = request.form['username']
        status &= cookie.gen(username)
    else:
        user = request.cookies.get('user')
        status &= cookie.parse(user) if user else cookie.gen("Ash")
    
    if status:
        status, username = cookie.get("username")

    error = None if status else str(cookie.error)
    if not status:
        cookie.gen('Ash')
        _,username = cookie.get("username")

    resp = make_response(
             render_template(
               "index.html", 
               username=username,
               error=error
             )
           )
    resp.set_cookie("user", cookie.cookie)
    return resp