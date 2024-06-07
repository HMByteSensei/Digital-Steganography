import numpy as np
from scipy.io import wavfile
from pydub import AudioSegment

def load_audio(file_path):
    audio = AudioSegment.from_wav(file_path)
    audio = audio.set_channels(1)  # konvertuj u mono zvuk
    sample_rate = audio.frame_rate
    samples = np.array(audio.get_array_of_samples())
    print(f"Učitan zvuk: {file_path}, Frekvencija uzorkovanja: {sample_rate}, Broj uzorka: {len(samples)}")
    return samples, sample_rate


def save_audio(samples, sample_rate, output_path):
    audio_segment = AudioSegment(
        samples.tobytes(),
        frame_rate=sample_rate,
        sample_width=samples.dtype.itemsize,
        channels=1
    )
    audio_segment.export(output_path, format="wav")
    print(f"Sačuvan izmijenjeni zvuk: {output_path}")


def string_to_binary(string):
    binary = ''.join(format(ord(char), '08b') for char in string)
    print(f"String u binarni: '{string}' -> {binary}")
    return binary


def binary_to_string(binary):
    if len(binary) % 8 != 0:
        raise ValueError("Dužina binarnog stringa nije višekratnik od 8")

    binary_values = [binary[i:i + 8] for i in range(0, len(binary), 8)]
    ascii_characters = [chr(int(binary_value, 2)) for binary_value in binary_values]
    result = ''.join(ascii_characters)
    print(f"Binarni u string: {binary} -> '{result}'")
    return result


def embed_string_in_audio(samples, secret_string):
    binary_string = string_to_binary(secret_string)
    samples_copy = samples.copy()

    print(f"Ugrađivanje binarnog stringa u zvuk: {binary_string}")

    # Provera kapaciteta audio zapisa
    if len(binary_string) > len(samples_copy):
        raise ValueError("Audio zapis nema dovoljno kapaciteta za ugradnju tajne poruke")

    # Provera dostupnog prostora za ugradnju
    available_space = len(samples_copy) // 8
    if len(secret_string) > available_space:
        raise ValueError("Nedovoljno prostora u audio zapisu za ugradnju tajne poruke")

    for i, bit in enumerate(binary_string):
        samples_copy[i] = (samples_copy[i] & ~1) | int(bit)

    print(f"Izmijenjeni broj uzorka: {len(samples_copy)}")
    return samples_copy


def extract_string_from_audio(samples, length):
    binary_string = ''.join([str(samples[i] & 1) for i in range(length * 8)])
    binary_string = binary_string[:length * 8]

    print(f"Izvučen binarni string: {binary_string}")

    if len(binary_string) % 8 != 0:
        raise ValueError("Dužina izvučenog binarnog stringa nije višekratnik od 8")

    secret_string = binary_to_string(binary_string)
    print(f"Dekodirani string: '{secret_string}'")
    return secret_string


# Učitavanje ulaznog zvuka
input_audio_path = "input_audio.wav"
output_audio_path = "output_audio.wav"
secret_message = "Nuclear"

samples, sample_rate = load_audio(input_audio_path)

# Ugrađivanje tajne poruke u zvuk
modified_samples = embed_string_in_audio(samples, secret_message)

# Čuvanje izmijenjenog zvuka
save_audio(modified_samples, sample_rate, output_audio_path)
save_audio(modified_samples, sample_rate, output_audio_path)

# Izdvajanje tajne poruke iz izmijenjenog zvuka
extracted_message = extract_string_from_audio(modified_samples, len(secret_message))
print("Izvučena poruka:", extracted_message)
