import PIL


class LeastSB():
    MAX_BIT_LENGTH = 16

    def __init__(self, img):
        self.size_x, self.size_y, self.size_channel = img.shape
        self.image = img
        self.cur_x = 0
        self.cur_y = 0
        self.cur_channel = 0

    def encode_image(self, c_image, secret_image):
        # Open the cover image and secret image
        cover_image = PIL.Image.open(c_image)
        secret_image = PIL.Image.open(secret_image)

        # Resize the secret image to match the cover image
        secret_image = secret_image.resize(cover_image.size)

        # Convert the cover image and secret image to RGB mode
        cover_image = cover_image.convert('RGB')
        secret_image = secret_image.convert('RGB')

        # Get the pixels of the cover image and secret image
        cover_pixels = cover_image.load()
        secret_pixels = secret_image.load()

        # Encode the secret image into the cover image using LSB technique
        for i in range(cover_image.size[0]):
            for j in range(cover_image.size[1]):
                cover_pixel = cover_pixels[i, j]
                secret_pixel = secret_pixels[i, j]
                r, g, b = cover_pixel
                sr, sg, sb = secret_pixel
                # Encode the secret image into the blue channel of the cover image
                encoded_pixel = (r, g, ((b & 254) | (sb >> 7)))
                cover_pixels[i, j] = encoded_pixel

        # Save the encoded image as a new file
        cover_image.save('encoded_image.png')
        return cover_image
        # messagebox.showinfo("Success", "Encoding completed successfully")

    def decode_image(self, image):
        # Open the encoded image
        encoded_image = PIL.Image.open(image)
        # Convert the encoded image to RGB mode
        encoded_image = encoded_image.convert('RGB')

        # Get the pixels of the encoded image
        encoded_pixels = encoded_image.load()

        # Decode the secret image from the encoded image using LSB technique
        secret_image = PIL.Image.new('RGB', encoded_image.size)
        secret_pixels = secret_image.load()
        for i in range(encoded_image.size[0]):
            for j in range(encoded_image.size[1]):
                encoded_pixel = encoded_pixels[i, j]
                r, g, b = encoded_pixel
                # Decode the secret image from the blue channel of the encoded image
                decoded_pixel = (0, 0, (b & 1) << 7)
                secret_pixels[i, j] = decoded_pixel

        return secret_image

   