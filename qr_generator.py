import qrcode
import os

def generate_qr(student_id):
    if not os.path.exists("qr_codes"):
        os.makedirs("qr_codes")

    img = qrcode.make(student_id)
    img.save(f"qr_codes/{student_id}.png")
