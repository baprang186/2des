from Crypto.Cipher import DES
import base64

# Ham tao doi tuong DES
def des_encrypt(key, plaintext):
    cipher = DES.new(key, DES.MODE_ECB)
    # Padding de dam bao plaintext co do dai boi so cua 8
    padded_text = plaintext + (8 - len(plaintext) % 8) * ' '
    encrypted = cipher.encrypt(padded_text.encode('utf-8'))
    return base64.b64encode(encrypted).decode('utf-8')

# Vi du su dung
key_input = input("Nhap khoa key: ").strip()
key = key_input.encode()
if len(key) % 8 != 0:
    raise ValueError("Khoa phai co do dai 8 byte!") 
plaintext = input("Nhap ban ro plaintext: ")

ciphertext = des_encrypt(key, plaintext)
print("Ciphertext: ", ciphertext)
