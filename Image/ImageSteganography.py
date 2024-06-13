import cv2
from Cryptography.TextCrypto import TextTransformer
import os
import numpy as np
import scipy.fftpack as fft

class imageSteganography:
    # ----------------------------------------------LSB----------------------------------------------------
    def encode_lsb(self, image_name, secret_data, to_encrypt):
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
        cv2.imwrite(image_name + "Result.png", image)
        # print("Secret data encoded")

    def extract_message_up_to_END(self, decoded_message):
        index = decoded_message.find("!END")
        if index != -1:
            return decoded_message[:index]
        else:
            return decoded_message

    def decode_lsb(self, image_path, to_encrypt):
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
        # print (secret_message)
        return secret_message
    #----------------------------------------------LSB----------------------------------------------------
    # ----------------------------------------------DCT----------------------------------------------------
    def string_to_binary(self, secret_string):
        return ''.join(format(ord(char), '08b') for char in secret_string)

    def binary_to_string(self, binary_string):
        chars = [binary_string[i:i + 8] for i in range(0, len(binary_string), 8)]
        return ''.join(chr(int(char, 2)) for char in chars)

    def encode_dct(self, image_path, secret_string, to_crypt, strength=0.1):
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  # load as grayscale

        # convert the message to binary
        binary_string = self.string_to_binary(secret_string)
        binary_string += '1000000000000001'  # my custom end-of-message delimiter

        # image to a 1D array
        flat_image = image.flatten()
        num_samples = len(flat_image)

        # applying DCT to the image
        dct_samples = fft.dct(flat_image, norm='ortho')
        step = int(num_samples / len(binary_string))

        # Embed the binary string into the DCT coefficients
        # print(binary_string)
        for i, bit in enumerate(binary_string):
            index = i * step
            if index < num_samples:
                if bit == '1':
                    dct_samples[index] += strength * np.max(dct_samples)
                else:
                    dct_samples[index] -= strength * np.max(dct_samples)

        # inverse DCT to get the modified image
        modified_samples = fft.idct(dct_samples, norm='ortho')
        modified_image = modified_samples.reshape(image.shape)
        modified_image = np.clip(modified_image, 0, 255)

        directory = os.path.dirname(image_path)
        # print(directory)
        cv2.imwrite(image_path + "Result.png", modified_image.astype(np.uint8))
        print("Message embedded successfully!")

    def decode_dct(self, image_path, message_length, to_crypt):
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        # again image to a 1D array
        flat_image = image.flatten()
        num_samples = len(flat_image)

        # DCT to the image
        dct_samples = fft.dct(flat_image, norm='ortho')
        step = int(num_samples / (message_length * 8 + 16))  # Account for the delimiter

        # get binary string from the DCT coefficients
        binary_string = ''
        print("Extracting binary string from image:")
        for i in range(message_length * 8 + 16):
            index = i * step
            if index < num_samples:
                if dct_samples[index] > 0:
                    binary_string += '1'
                else:
                    binary_string += '0'

        # remove the end-of-message delimiter
        binary_string = binary_string[:binary_string.find('1000000000000001')]
        # print(f"Extracted binary string: {binary_string}")

        # converting binary string to the original message
        secret_string = self.binary_to_string(binary_string)
        # print(secret_string)
        return secret_string

    # ----------------------------------------------DCT----------------------------------------------------
    def engine(self, filename, text, method, to_crypt, reverse, length=11):
        result = ""
        if method == "LSB":
            if reverse is False:
                self.encode_lsb(filename, text, to_crypt)
            else:
                result = self.decode_lsb(filename, to_crypt)
        else:
            if reverse is False:
                self.encode_dct(filename, text, to_crypt)
            else:
                # print("LENGTH: " + str(length))
                result = self.decode_dct(filename, length, to_crypt)

        print(result)
        if reverse is True:
            try:
                with open(filename + "Result.txt", 'w', encoding='latin-1') as file:
                    file.write(result)
            except:
                return "Cover text is too short or it does not have all letters that are copntained in secret text."
        return True