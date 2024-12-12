import base64
from Crypto.Cipher import DES

# Ham ma hoa DES
def des_encrypt(key, plaintext):
    cipher = DES.new(key, DES.MODE_ECB)
    padded_text = plaintext + (8 - len(plaintext) % 8) * ' '
    encrypted = cipher.encrypt(padded_text.encode('utf-8'))
    return base64.b64encode(encrypted).decode('utf-8')

# Ham giai ma DES
def des_decrypt(key, ciphertext):
    cipher = DES.new(key, DES.MODE_ECB)
    encrypted_bytes = base64.b64decode(ciphertext)
    try:
        decrypted = cipher.decrypt(encrypted_bytes)
        return decrypted.decode('utf-8').rstrip()
    except UnicodeDecodeError:
        return ""

# Ham tan cong DES
def des_attack(ciphertext, plaintext, keys_file):
    with open(keys_file, 'r') as f:
        keys = [line.strip().encode('utf-8') for line in f.readlines()]
    
    print(f"Start testing key in {keys_file}...")
    for key in keys:
        decrypted = des_decrypt(key, ciphertext)
        print(f"Test key: {key.decode('utf-8')} -> Decrypted: {decrypted}")
        if decrypted == plaintext:
            return key
    return None

#  Meet-in-the-Middle
def meet_in_the_middle_attack(ciphertext, plaintext, keys1_file, keys2_file):
    # Doc khoa tu file
    with open(keys1_file, 'r') as f:
        keys1 = [line.strip().encode('utf-8') for line in f.readlines()]
    with open(keys2_file, 'r') as f:
        keys2 = [line.strip().encode('utf-8') for line in f.readlines()]

    if not keys1 or not keys2:  # Kiem tra rỗng
        print("Mot trong 2 file key rong. Chuyen sang tan cong DES")
        keys_file = keys1_file if keys1 else keys2_file
        found_key = des_attack(ciphertext, plaintext, keys_file)
        if found_key:
            print("\nTan cong DES thanh cong!")
            print(f"Found key: {found_key.decode('utf-8')}")
        else:
            print("\nTan cong DES that bai. Khong tim duoc khoa phu hop!")
        return None, None  # Không thực hiện MITM nếu một trong hai file rỗng

    # Luu plaintext voi tat ca key1
    encrypt_dict = {}
    print("Thu key trong keys1.txt...")
    for key1 in keys1:
        encrypted = des_encrypt(key1, plaintext)
        encrypt_dict[encrypted] = key1
        print(f"Thu key1: {key1.decode('utf-8')} -> Encrypted: {encrypted}")

    # Kiem tra ciphertext voi tat ca key2
    print("\nThu key trong keys2.txt...")
    for key2 in keys2:
        decrypted = des_decrypt(key2, ciphertext)
        print(f"Thu key2: {key2.decode('utf-8')} -> Decrypted: {decrypted}")
        if decrypted in encrypt_dict:
            return encrypt_dict[decrypted], key2

    return None, None

if __name__ == "__main__":
    # Cac file keys1.txt và keys2.txt
    keys1_file = "keys1.txt"
    keys2_file = "keys2.txt"

    # Thiet lap khoa và plaintext
    plaintext= input("Nhap plaintext (dang chuoi, vi du: Hello123): ").strip()

    ciphertext= input("Nhap ciphertext: ").strip()

    # Tan cong Meet-in-the-Middle
    found_key1, found_key2 = meet_in_the_middle_attack(ciphertext, plaintext, keys1_file, keys2_file)

    if found_key1 and found_key2:
        print("\nTan cong 2DES thanh cong. Key tim duoc: ")
        print("Key1:", found_key1.decode('utf-8'))
        print("Key2:", found_key2.decode('utf-8'))
    else:
        print("\nTan cong 2DES that bai. Khong tim duoc cap khoa phu hop!")
