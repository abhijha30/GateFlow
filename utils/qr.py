import qrcode

def generate_qr(data, path):
    img = qrcode.make(data)
    img.save(path)
    return path
