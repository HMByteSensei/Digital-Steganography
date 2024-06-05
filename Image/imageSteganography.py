import cv2
from Cryptography.TextCrypto import TextTransformer

class imageSteganography:
    def encode(self, image_name, secret_data, to_encrypt):
        # Read the image
        image = cv2.imread(image_name)

        if to_encrypt is True:
            textTransformer = TextTransformer()
            secret_data = textTransformer.txt_encrypt(secret_data) + "!END"
            print(secret_data)
        # Calculate the maximum bytes we can encode to later see if we can encode secret data into image
        n_bytes = image.shape[0] * image.shape[1] * 3 // 8
        print("Maximum bytes to encode:", n_bytes)

        # Check if secret data fits within the image
        if len(secret_data) > n_bytes:
            raise ValueError("Secret data is too large for the image")

        # Convert secret data to binary
        secret_binary = ''.join(format(ord(char), '08b') for char in secret_data)

        # Embed the secret data into the image
        idx = 0
        for row in image:
            for pixel in row:
                for color_channel in range(3):
                    if idx < len(secret_binary):
                        pixel[color_channel] = pixel[color_channel] & ~1 | int(secret_binary[idx])
                        idx += 1

        # Saving modified image
        cv2.imwrite("encoded_image.png", image)
        print("Secret data encoded successfully!")

    def extract_message_up_to_END(self, decoded_message):
        index = decoded_message.find("!END")
        if index != -1:
            return decoded_message[:index]
        else:
            return decoded_message

    def decode(self, image_path, to_encrypt):
        # Read the encoded image
        encoded_image = cv2.imread(image_path)

        secret_binary = ""
        # Extract the LSB from each pixel
        for row in encoded_image:
            for pixel in row:
                for color_channel in range(3):
                    secret_bit = pixel[color_channel] & 1
                    secret_binary += str(secret_bit)

        # Convert binary to text
        secret_message = ""
        for i in range(0, len(secret_binary), 8):
            byte = secret_binary[i:i + 8]
            secret_message += chr(int(byte, 2))

        if to_encrypt is True:
            textTransformer = TextTransformer()
            secret_message = textTransformer.txt_decrypt(self.extract_message_up_to_END(secret_message))
        return secret_message