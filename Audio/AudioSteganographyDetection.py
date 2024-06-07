import numpy as np
from scipy.io import wavfile
from pydub import AudioSegment

def load_audio(file_path):
    audio = AudioSegment.from_wav(file_path)
    audio = audio.set_channels(1)  # Convert to mono
    sample_rate = audio.frame_rate
    samples = np.array(audio.get_array_of_samples())
    print(f"Loaded audio file: {file_path}, Sampling rate: {sample_rate}, Number of samples: {len(samples)}")
    return samples, sample_rate

def extract_author_code_from_audio(samples, length):
    binary_code = ''.join([str(samples[i] & 1) for i in range(length * 8)])
    binary_code = binary_code[:length * 8]

    # Convert binary code to string letters
    signature_text = ''.join(chr(int(binary_code[i:i + 8], 2)) for i in range(0, len(binary_code), 8))

    return signature_text

def compare_codes(original_code, extracted_code):
    print("Original author code:", original_code)
    print("Extracted author code:", extracted_code)
    if original_code == extracted_code:
        print("Embedded code matches the original author code.")
    else:
        print("Embedded code does not match the original author code.")

# Original author code
original_author_code = "Nuclear"

# Path to the audio file from which the signature is extracted
input_audio_path = "output_audio.wav"

# Load audio file
samples, _ = load_audio(input_audio_path)

# Extract code from audio recording
extracted_code = extract_author_code_from_audio(samples, len(original_author_code))

# Compare with the original code
compare_codes(original_author_code, extracted_code)

