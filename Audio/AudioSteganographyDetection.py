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


def extract_author_code_from_audio(samples, length):
    binary_code = ''.join([str(samples[i] & 1) for i in range(length * 8)])
    binary_code = binary_code[:length * 8]

    # Pretvori binarni kod u string slova
    signature_text = ''.join(chr(int(binary_code[i:i + 8], 2)) for i in range(0, len(binary_code), 8))

    return signature_text


def compare_codes(original_code, extracted_code):
    print("Originalni kod autora:", original_code)
    print("Ekstraktovani kod autora:", extracted_code)
    if original_code == extracted_code:
        print("Ugrađeni Kod se poklapa sa originalnim kodom autora.")
    else:
        print("Ugrađeni Kod se ne poklapa sa originalnim kodom autora.")


# Originalni otisak autora
original_author_code = "Nuclear"

# Putanja do audio fajla iz kog se vadi otisak
input_audio_path = "output_audio.wav"

# Učitaj audio datoteku
samples, _ = load_audio(input_audio_path)

# Izvuci kod iz audio zapisa
extracted_code = extract_author_code_from_audio(samples, len(original_author_code))

# Uporedi sa originalnim kodom
compare_codes(original_author_code, extracted_code)
