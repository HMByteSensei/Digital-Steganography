import numpy as np
import scipy.fftpack as fft
from scipy.io import wavfile
from pydub import AudioSegment
from Audio.AudioSteganographyDCT import dct_extract

extraction_attempted = False
def load_audio(file_path):
    audio = AudioSegment.from_wav(file_path)
    audio = audio.set_channels(1)  # Convert to mono
    sample_rate = audio.frame_rate
    samples = np.array(audio.get_array_of_samples())
    print(f"Loaded audio file: {file_path}, Sampling rate: {sample_rate}, Number of samples: {len(samples)}")
    return samples, sample_rate

def extract_author_code(samples, length):
    binary_code = ''.join([str(samples[i] & 1) for i in range(length * 8)])
    binary_code = binary_code[:length * 8]
    # Convert binary code to string letters
    code_text = ''.join(chr(int(binary_code[i:i + 8], 2)) for i in range(0, len(binary_code), 8))
    return code_text

def binary_to_string(binary):
    if len(binary) % 8 != 0:
        raise ValueError("Length of binary string is not a multiple of 8")

    binary_values = [binary[i:i + 8] for i in range(0, len(binary), 8)]
    ascii_characters = [chr(int(binary_value, 2)) for binary_value in binary_values]
    result = ''.join(ascii_characters)
    print(f"Binary to string: {binary} -> '{result}'")
    return result

def compare_codes(original_code, extracted_code):
    global extraction_attempted
    print("Original author code:", original_code)
    print("Extracted author code:", extracted_code)
    if original_code == extracted_code:
        print("Embedded code matches the original author code.")
    else:
        print("Embedded code doesn't match the original author code.")
        if not extraction_attempted:
            extraction_attempted = True
            extracted_code = dct_extract(samples, len(original_author_code))
            compare_codes(original_author_code, extracted_code)

# Original author code
original_author_code = "Nuclear"

# Path to the audio file from which the signature is extracted
input_audio_path = "output_audio.wav"

# Load audio file
samples, _ = load_audio(input_audio_path)

# Extract code from audio recording
extracted_code = extract_author_code(samples, len(original_author_code))

# Compare with the original code
compare_codes(original_author_code, extracted_code)
