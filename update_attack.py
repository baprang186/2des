import base64
from Crypto.Cipher import DES

# Hàm mã hóa DES
def des_encrypt(key, plaintext):
    cipher = DES.new(key, DES.MODE_ECB)
    padded_text = plaintext + (8 - len(plaintext) % 8) * ' '
    encrypted = cipher.encrypt(padded_text.encode('utf-8'))
    return base64.b64encode(encrypted).decode('utf-8')

# Hàm giải mã DES
def des_decrypt(key, ciphertext):
    cipher = DES.new(key, DES.MODE_ECB)
    encrypted_bytes = base64.b64decode(ciphertext)
    try:
        decrypted = cipher.decrypt(encrypted_bytes)
        return decrypted.decode('utf-8').rstrip()
    except UnicodeDecodeError:
        return ""

# Hàm tấn công DES
def des_attack(ciphertext, plaintext, keys_file):
    with open(keys_file, 'r') as f:
        keys = [line.strip().encode('utf-8') for line in f.readlines()]
    
    print(f"Bắt đầu thử khóa trong {keys_file}...")
    for key in keys:
        decrypted = des_decrypt(key, ciphertext)
        print(f"Thử key: {key.decode('utf-8')} -> Giải mã: {decrypted}")
        if decrypted == plaintext:
            return key
    return None

# Hàm tấn công Meet-in-the-Middle
def meet_in_the_middle_attack(ciphertext, plaintext, keys1_file, keys2_file):
    # Đọc danh sách khóa từ file
    with open(keys1_file, 'r') as f:
        keys1 = [line.strip().encode('utf-8') for line in f.readlines()]
    with open(keys2_file, 'r') as f:
        keys2 = [line.strip().encode('utf-8') for line in f.readlines()]

    if not keys1 or not keys2:  # Kiểm tra nếu keys1 hoặc keys2 rỗng
        print("Một trong hai file khóa rỗng. Chuyển sang tấn công DES đơn.")
        keys_file = keys1_file if keys1 else keys2_file
        found_key = des_attack(ciphertext, plaintext, keys_file)
        if found_key:
            print("\nTấn công DES thành công ")
            print(f"Khóa tìm được: {found_key.decode('utf-8')}")
        else:
            print("\nTấn công DES không thành công. Không tìm thấy khóa phù hợp!")
        return None, None  # Không thực hiện MITM nếu một trong hai file rỗng

    # Lưu kết quả mã hóa plaintext với tất cả key1
    encrypt_dict = {}
    print("Bắt đầu thử khóa trong keys1.txt...")
    for key1 in keys1:
        encrypted = des_encrypt(key1, plaintext)
        encrypt_dict[encrypted] = key1
        print(f"Thử key1: {key1.decode('utf-8')} -> Mã hóa: {encrypted}")

    # Kiểm tra giải mã ciphertext với tất cả key2
    print("\nBắt đầu thử khóa trong keys2.txt...")
    for key2 in keys2:
        decrypted = des_decrypt(key2, ciphertext)
        print(f"Thử key2: {key2.decode('utf-8')} -> Giải mã: {decrypted}")
        if decrypted in encrypt_dict:
            return encrypt_dict[decrypted], key2

    return None, None

# Chương trình chính
if __name__ == "__main__":
    # Tạo các file khóa (cần chuẩn bị trước keys1.txt và keys2.txt)
    keys1_file = "keys1.txt"
    keys2_file = "keys2.txt"

    # Thiết lập cặp khóa và plaintext
    plaintext= input("Nhập plaintext (dạng chuỗi, ví dụ: Hello123): ").strip()

    ciphertext= input("Nhập ciphertext: ").strip()

    # Tấn công Meet-in-the-Middle
    found_key1, found_key2 = meet_in_the_middle_attack(ciphertext, plaintext, keys1_file, keys2_file)

    if found_key1 and found_key2:
        print("\nTấn công 2DES thành công.  Khóa tìm được:")
        print("Key1:", found_key1.decode('utf-8'))
        print("Key2:", found_key2.decode('utf-8'))
    else:
        print("\nTấn công 2DES không thành công. Không tìm thấy cặp khóa phù hợp!")
