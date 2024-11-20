from Crypto.Cipher import DES
import base64

# Hàm tạo đối tượng DES
def des_encrypt(key, plaintext):
    cipher = DES.new(key, DES.MODE_ECB)
    # Padding để đảm bảo plaintext có độ dài là bội số của 8
    padded_text = plaintext + (8 - len(plaintext) % 8) * ' '
    encrypted = cipher.encrypt(padded_text.encode('utf-8'))
    return base64.b64encode(encrypted).decode('utf-8')

def des_decrypt(key, ciphertext):
    cipher = DES.new(key, DES.MODE_ECB)
    encrypted_bytes = base64.b64decode(ciphertext)
    decrypted = cipher.decrypt(encrypted_bytes)
    return decrypted.decode('utf-8').rstrip()

def double_des_encrypt(key1, key2, plaintext):
    # Mã hóa lần 1 với key1
    intermediate = des_encrypt(key1, plaintext)
    # Mã hóa lần 2 với key2
    return des_encrypt(key2, intermediate)

def double_des_decrypt(key1, key2, ciphertext):
    # Giải mã lần 1 với key2
    intermediate = des_decrypt(key2, ciphertext)
    # Giải mã lần 2 với key1
    return des_decrypt(key1, intermediate)

# Ví dụ sử dụng
key1_input = input("Nhập khóa key1: ").strip()
key1 = key1_input.encode()
if len(key1) % 8 != 0:
    raise ValueError("Khóa phải có độ dài 8 byte!") 
key2_input = input("Nhập khóa key: ").strip()
key2 = key2_input.encode()
if len(key2) % 8 != 0:
    raise ValueError("Khóa phải có độ dài 8 byte!") 
#key1 = b'key1key1'  # Khóa 1
#key2 = b'key2key2'  # Khóa 2

plaintext = input("Enter plaintext: ")
ciphertext = double_des_encrypt(key1, key2, plaintext)
print("Ciphertext (2DES):", ciphertext)

decrypted_text = double_des_decrypt(key1, key2, ciphertext)
print("Decrypted text (2DES):", decrypted_text)
