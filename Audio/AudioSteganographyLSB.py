import numpy as np
from scipy.io import wavfile
from pydub import AudioSegment

def load_audio(file_path):
    audio = AudioSegment.from_wav(file_path)
    audio = audio.set_channels(1)  # Pretvori u mono
    sample_rate = audio.frame_rate
    samples = np.array(audio.get_array_of_samples())
    print(f"Učitana audio datoteka: {file_path}, Brzina uzorkovanja: {sample_rate}, Broj uzoraka: {len(samples)}")
    return samples, sample_rate

def save_audio(samples, sample_rate, output_path):
    audio_segment = AudioSegment(
        samples.tobytes(),
        frame_rate=sample_rate,
        sample_width=samples.dtype.itemsize,
        channels=1
    )
    audio_segment.export(output_path, format="wav")
    print(f"Sačuvana izmijenjena audio datoteka: {output_path}")

def string_to_binary(string):
    binary = ''.join(format(ord(char), '08b') for char in string)
    print(f"String u binarni: '{string}' -> {binary}")
    return binary

def binary_to_string(binary):
    if len(binary) % 8 != 0:
        raise ValueError("Dužina binarnog stringa nije višekratnik broja 8")

    binary_values = [binary[i:i + 8] for i in range(0, len(binary), 8)]
    ascii_characters = [chr(int(binary_value, 2)) for binary_value in binary_values]
    result = ''.join(ascii_characters)
    print(f"Binarni u string: {binary} -> '{result}'")
    return result

def embed_string_in_audio(samples, sample_rate, secret_string):
    binary_string = string_to_binary(secret_string)
    samples_copy = samples.copy()

    print(f"Ugrađivanje binarnog stringa u audio: {binary_string}")
    for i, bit in enumerate(binary_string):
        samples_copy[i] = (samples_copy[i] & ~1) | int(bit)

    print(f"Izmijenjeni broj uzoraka: {len(samples_copy)}")
    return samples_copy

def extract_string_from_audio(samples, sample_rate, length):
    binary_string = ''.join([str(samples[i] & 1) for i in range(length * 8)])
    binary_string = binary_string[:length * 8]

    print(f"Izvučeni binarni string: {binary_string}")

    if len(binary_string) % 8 != 0:
        raise ValueError("Dužina izvučenog binarnog stringa nije višekratnik broja 8")

    secret_string = binary_to_string(binary_string)
    print(f"Dekodirani string: '{secret_string}'")
    return secret_string


# Primer korišćenja
input_audio_path = "input_audio.wav"
output_audio_path = "output_audio.wav"
secret_message = "Nuclear"

# Korak 1: Učitaj audio datoteku
samples, sample_rate = load_audio(input_audio_path)

# Korak 2: Ugradi tajnu poruku
modified_samples = embed_string_in_audio(samples, sample_rate, secret_message)

# Korak 3: Sačuvaj izmijenjeni audio zapis
save_audio(modified_samples, sample_rate, output_audio_path)

# Korak 4: Izvuci tajnu poruku iz izmijenjenog audio zapisa
extracted_message = extract_string_from_audio(modified_samples, sample_rate, len(secret_message))
print("Izvučena poruka:", extracted_message)

