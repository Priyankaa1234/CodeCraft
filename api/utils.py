import qrcode
import os
from django.conf import settings

def generate_qr_code(doc_uid):
    url = f"http://127.0.0.1:8000/api/scan/{doc_uid}/" # can replace with production URL
    img = qrcode.make(url)
    save_path = os.path.join(settings.MEDIA_ROOT, 'qrcodes')
    os.makedirs(save_path, exist_ok=True)

    file_path = os.path.join(save_path, f'{doc_uid}.png')
    img.save(file_path)
    return f"{settings.MEDIA_URL}qrcodes/{doc_uid}.png"
