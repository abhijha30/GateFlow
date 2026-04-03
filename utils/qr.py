import qrcode
import os

def generate_qr(data, path="qr_codes"):
    # 📁 create folder if not exists
    if not os.path.exists(path):
        os.makedirs(path)

    file_path = f"{path}/{data}.png"

    img = qrcode.make(data)
    img.save(file_path)

    return file_path
