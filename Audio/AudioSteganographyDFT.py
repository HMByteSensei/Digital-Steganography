import numpy as np
from scipy.io import wavfile
from pydub import AudioSegment

def load_audio(file_path):
    audio = AudioSegment.from_wav(file_path)
    audio = audio.set_channels(1)  # convert to mono sound
    sample_rate = audio.frame_rate
    samples = np.array(audio.get_array_of_samples())
    print(f"Loaded sound: {file_path}, Sampling frequency: {sample_rate}, Number of samples: {len(samples)}")
    return samples, sample_rate

def save_audio(samples, sample_rate, output_path):
    audio_segment = AudioSegment(
        samples.tobytes(),
        frame_rate=sample_rate,
        sample_width=samples.dtype.itemsize,
        channels=1
    )
    audio_segment.export(output_path, format="wav")
    print(f"Saved modified sound: {output_path}")

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

def embed_string_in_audio(samples, secret_string):
    binary_string = string_to_binary(secret_string)
    samples_copy = samples.copy()

    print(f"Embedding binary string into sound: {binary_string}")

    # Check audio capacity
    if len(binary_string) > len(samples_copy):
        raise ValueError("Audio does not have enough capacity to embed secret message")

    # Check available embedding space
    available_space = len(samples_copy) // 8
    if len(secret_string) > available_space:
        raise ValueError("Insufficient space in audio for embedding secret message")

    for i, bit in enumerate(binary_string):
        samples_copy[i] = (samples_copy[i] & ~1) | int(bit)

    print(f"Number of modified samples: {len(samples_copy)}")
    return samples_copy

def extract_string_from_audio(samples, length):
    binary_string = ''.join([str(samples[i] & 1) for i in range(length * 8)])
    binary_string = binary_string[:length * 8]

    print(f"Extracted binary string: {binary_string}")

    if len(binary_string) % 8 != 0:
        raise ValueError("Length of extracted binary string is not a multiple of 8")

    secret_string = binary_to_string(binary_string)
    print(f"Decoded string: '{secret_string}'")
    return secret_string

# Load input sound
input_audio_path = "input_audio.wav"
output_audio_path = "output_audio.wav"
secret_message = "Nuclear"

samples, sample_rate = load_audio(input_audio_path)

# Embedding secret message into sound
modified_samples = embed_string_in_audio(samples, secret_message)

# Save modified sound
save_audio(modified_samples, sample_rate, output_audio_path)

# Extract secret message from modified sound
extracted_message = extract_string_from_audio(modified_samples, len(secret_message))
print("Extracted message:", extracted_message)
