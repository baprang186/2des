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

# Ví dụ sử dụng
key = b'key00002'  # Khóa phải có độ dài 8 byte
plaintext = "Hello, DES!"

ciphertext = des_encrypt(key, plaintext)
print("Ciphertext:", ciphertext)

decrypted_text = des_decrypt(key, ciphertext)
print("Decrypted text:", decrypted_text)
