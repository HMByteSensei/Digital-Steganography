import cv2
import numpy as np

def load_video(file_path):
    cap = cv2.VideoCapture(file_path)
    frames = []
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    cap.release()
    print(f"Loaded video file: {file_path}, Number of frames: {len(frames)}")
    return frames

def save_video(frames, output_path, fps):
    height, width, layers = frames[0].shape
    size = (width, height)
    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'XVID'), fps, size)
    for frame in frames:
        out.write(frame)
    out.release()
    print(f"Saved modified video file: {output_path}")

def string_to_binary(string):
    binary = ''.join(format(ord(char), '08b') for char in string)
    print(f"String to binary: '{string}' -> {binary}")
    return binary

def binary_to_string(binary):
    binary_values = [binary[i:i + 8] for i in range(0, len(binary), 8)]
    ascii_characters = [chr(int(binary_value, 2)) for binary_value in binary_values]
    result = ''.join(ascii_characters)
    print(f"Binary to string: {binary} -> '{result}'")
    return result

def lsb_embed(frames, secret_string):
    binary_string = string_to_binary(secret_string) + '00000000'  # End delimiter
    binary_index = 0
    for frame in frames:
        for row in frame:
            for pixel in row:
                for channel in range(3):  # Assuming RGB
                    if binary_index < len(binary_string):
                        pixel[channel] = (pixel[channel] & ~1) | int(binary_string[binary_index])
                        binary_index += 1
                    else:
                        return frames
    print(f"Embedded binary string into video frames")
    return frames

def lsb_extract(frames):
    binary_string = ''
    for frame in frames:
        for row in frame:
            for pixel in row:
                for channel in range(3):
                    binary_string += str(pixel[channel] & 1)
                    if len(binary_string) % 8 == 0 and binary_string[-8:] == '00000000':  # End delimiter
                        return binary_to_string(binary_string[:-8])
    return binary_to_string(binary_string)

# Example usage
input_video_path = "input_video.avi"
output_video_path = "output_video.avi"
secret_message = "Nuclear"

# Step 1: Load the video file
frames = load_video(input_video_path)

# Step 2: Embed the secret message
modified_frames = lsb_embed(frames, secret_message)

# Step 3: Save the modified video file
save_video(modified_frames, output_video_path, 30)

# Step 4: Extract the secret message from the modified video file
extracted_message = lsb_extract(modified_frames)
print("Extracted message:", extracted_message)