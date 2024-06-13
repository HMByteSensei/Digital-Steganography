import cv2, os
import numpy as np
import scipy.fftpack as fft
from Cryptography.TextCrypto import TextTransformer

def string_to_binary(secret_string):
    return ''.join(format(ord(char), '08b') for char in secret_string)

def binary_to_string(binary_string):
    chars = [binary_string[i:i+8] for i in range(0, len(binary_string), 8)]
    return ''.join(chr(int(char, 2)) for char in chars)

def dct_embed(image_path, secret_string, strength=0.1):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  # load as grayscale

    # convert the message to binary
    binary_string = string_to_binary(secret_string)
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

def dct_extract(image_path, message_length):
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
    secret_string = binary_to_string(binary_string)
    # print(secret_string)
    return secret_string

# # Example usage
embed_message = "NEka tajna poruka neka"

# extracted_message = dct_extract('encoded_image.png', len(embed_message))
# extracted_message = t.rotate_decrypt(extracted_message)
# print("Extracted Message:", extracted_message)

# embed_message('C:\\Users\HM_codex\Pictures\Screenshots\Screenshot (38).png', 'Hello, world!')
# extracted_message = extract_message('modified_image.png', len('Hello, world!'))

dct_embed('C:\\Users\HM_codex\Pictures\\Snimak ekrana (24).png', embed_message)
extracted_message = dct_extract('C:\\Users\HM_codex\Pictures\Snimak ekrana (24).pngResult.png', len(embed_message))
print("Extracted Message:", extracted_message)