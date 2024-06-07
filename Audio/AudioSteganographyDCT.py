import numpy as np
import scipy.fftpack as fft
from scipy.io import wavfile
from pydub import AudioSegment

def load_audio(file_path):
    audio = AudioSegment.from_wav(file_path)
    audio = audio.set_channels(1)  # Convert to mono
    sample_rate = audio.frame_rate
    samples = np.array(audio.get_array_of_samples())
    print(f"Loaded audio file: {file_path}, Sampling rate: {sample_rate}, Number of samples: {len(samples)}")
    return samples, sample_rate

def save_audio(samples, sample_rate, output_path):
    audio_segment = AudioSegment(
        samples.tobytes(),
        frame_rate=sample_rate,
        sample_width=samples.dtype.itemsize,
        channels=1
    )
    audio_segment.export(output_path, format="wav")
    print(f"Saved modified audio file: {output_path}")

def string_to_binary(string):
    binary = ''.join(format(ord(char), '08b') for char in string)
    print(f"String to binary: '{string}' -> {binary}")
    return binary

def binary_to_string(binary):
    if len(binary) % 8 != 0:
        raise ValueError("Length of binary string is not a multiple of 8")

    binary_values = [binary[i:i + 8] for i in range(0, len(binary), 8)]
    ascii_characters = [chr(int(binary_value, 2)) for binary_value in binary_values]
    result = ''.join(ascii_characters)
    print(f"Binary to string: {binary} -> '{result}'")
    return result

def dct_embed(samples, secret_string, strength=0.1):
    binary_string = string_to_binary(secret_string)
    num_samples = len(samples)
    dct_samples = fft.dct(samples, norm='ortho')
    step = int(num_samples / len(binary_string))

    print(f"Embedding binary string into audio: {binary_string}")
    for i, bit in enumerate(binary_string):
        index = i * step
        if index < num_samples:
            if bit == '1':
                dct_samples[index] += strength * np.max(dct_samples)
            else:
                dct_samples[index] -= strength * np.max(dct_samples)

    modified_samples = fft.idct(dct_samples, norm='ortho')
    print(f"Number of modified samples: {len(modified_samples)}")
    return modified_samples.astype(np.int16)

def dct_extract(samples, length):
    num_samples = len(samples)
    dct_samples = fft.dct(samples, norm='ortho')
    step = int(num_samples / (length * 8))

    binary_string = ''
    print("Extracting binary string from audio:")
    for i in range(length * 8):
        index = i * step
        if index < num_samples:
            if dct_samples[index] > 0:
                binary_string += '1'
            else:
                binary_string += '0'

    print(f"Extracted binary string: {binary_string}")
    secret_string = binary_to_string(binary_string)
    print(f"Decoded string: '{secret_string}'")
    return secret_string


# Example usage
input_audio_path = "input_audio.wav"
output_audio_path = "output_audio.wav"
secret_message = "Nuclear"

# Step 1: Load the audio file
samples, sample_rate = load_audio(input_audio_path)

# Step 2: Embed the secret message
modified_samples = dct_embed(samples, secret_message)

# Step 3: Save the modified audio file
save_audio(modified_samples, sample_rate, output_audio_path)

# Step 4: Extract the secret message from the modified audio file
extracted_message = dct_extract(modified_samples, len(secret_message))
print("Extracted message:", extracted_message)
