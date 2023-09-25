from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from PIL import Image
import numpy as np
import os


class AESCipher:

    def __init__(self, key, iv):
        self.key = key
        self.iv = iv

    def encrypt_image(self, secret_image_path):

        # Load the secret image
        secret_image = Image.open(secret_image_path)
        img_size = secret_image.size
        img_mode = secret_image.mode

        # Convert the image to bytes
        secret_image_bytes = secret_image.tobytes()

        # Create the AES cipher object
        cipher = AES.new(self.key.encode(), AES.MODE_CBC, self.iv.encode())

        # Encrypt the image bytes
        encrypted_image_bytes = cipher.encrypt(
            pad(secret_image_bytes, AES.block_size))

        # Create a new image from the encrypted bytes
        encrypted_image = Image.frombytes(
            secret_image.mode, secret_image.size, encrypted_image_bytes)

        encrypted_path = os.path.splitext(secret_image_path)[0] + '_encrypted' + os.path.splitext(secret_image_path)[1]
        with open(encrypted_path, 'wb') as file:
            file.write(encrypted_image_bytes)
        return img_size, img_mode, encrypted_image, encrypted_image_bytes

    def decrypt_image(self, encrypted_image):
        cipher = AES.new(self.key, AES.MODE_CBC)
        return unpad(cipher.decrypt(encrypted_image), AES.block_size)
