import cv2
import numpy as np
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

def load_video(file_path, size=None):
    start_time = time.time()
    cap = cv2.VideoCapture(file_path)
    frames = []
    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if size is not None:
            frame = cv2.resize(frame, size, interpolation=cv2.INTER_LINEAR)
        frames.append(frame)
        frame_count += 1
        if frame_count % 100 == 0:
            print(f"Loaded {frame_count} frames...")
    cap.release()
    end_time = time.time()
    print(f"Loaded video file: {file_path}, Number of frames: {len(frames)}, Resolution: {frames[0].shape[1]}x{frames[0].shape[0]} in {end_time - start_time:.2f} seconds")
    return frames

def save_video(frames, output_path, fps):
    start_time = time.time()
    height, width, layers = frames[0].shape
    size = (width, height)
    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'XVID'), fps, size)
    frame_count = 0
    for frame in frames:
        out.write(frame)
        frame_count += 1
        if frame_count % 100 == 0:
            print(f"Saved {frame_count} frames...")
    out.release()
    end_time = time.time()
    print(f"Saved modified video file: {output_path} in {end_time - start_time:.2f} seconds")

def frame_to_binary_np(frame):
    return np.unpackbits(frame)

def binary_to_frame_np(binary, height, width):
    return np.packbits(binary).reshape((height, width, 3))

def lsb_embed(carrier_frames, secret_frames):
    start_time = time.time()
    with ThreadPoolExecutor() as executor:
        secret_binaries = list(executor.map(frame_to_binary_np, secret_frames))
    secret_binary = np.concatenate(secret_binaries)
    secret_binary = np.append(secret_binary, np.zeros(64, dtype=np.uint8))  # End delimiter

    binary_index = 0
    for frame_index, frame in enumerate(carrier_frames):
        flat_frame = frame.flatten()
        for i in range(len(flat_frame)):
            if binary_index < len(secret_binary):
                flat_frame[i] = (flat_frame[i] & ~1) | secret_binary[binary_index]
                binary_index += 1
            else:
                carrier_frames[frame_index] = flat_frame.reshape(frame.shape)
                end_time = time.time()
                print(f"Embedding completed in {end_time - start_time:.2f} seconds")
                return carrier_frames
        carrier_frames[frame_index] = flat_frame.reshape(frame.shape)
        if frame_index % 10 == 0:
            print(f"Processed {frame_index} frames for embedding...")
    end_time = time.time()
    print(f"Embedded secret video into carrier video frames in {end_time - start_time:.2f} seconds")
    return carrier_frames

def lsb_extract(carrier_frames, secret_height, secret_width):
    binary_string = np.zeros(len(carrier_frames) * carrier_frames[0].size, dtype=np.uint8)
    binary_index = 0
    start_time = time.time()
    for frame_index, frame in enumerate(carrier_frames):
        flat_frame = frame.flatten()
        bits = flat_frame & 1
        binary_string[binary_index:binary_index + len(bits)] = bits
        binary_index += len(bits)
        if binary_index >= 64 and np.array_equal(binary_string[binary_index-64:binary_index], np.zeros(64, dtype=np.uint8)):
            secret_binaries = binary_string[:binary_index-64]
            num_frames = len(secret_binaries) // (secret_height * secret_width * 24)
            secret_frames = [binary_to_frame_np(secret_binaries[i * secret_height * secret_width * 24:(i + 1) * secret_height * secret_width * 24], secret_height, secret_width) for i in range(num_frames)]
            end_time = time.time()
            print(f"Extraction completed in {end_time - start_time:.2f} seconds")
            return secret_frames
        if frame_index % 10 == 0:
            print(f"Processed {frame_index} frames for extraction...")
    end_time = time.time()
    print(f"Extracted frames in {end_time - start_time:.2f} seconds")
    return []

# Example usage
carrier_video_path = "input_video.avi"
secret_video_path = "secret_video.avi"
output_video_path = "output_video.avi"

# Define new resolution size for 360p (640x360)
new_resolution = (640, 360)

# Step 1: Load both videos with new resolution
start_time = time.time()
carrier_frames = load_video(carrier_video_path, new_resolution)
secret_frames = load_video(secret_video_path, new_resolution)
end_time = time.time()
print(f"Loading videos took {end_time - start_time:.2f} seconds")

# Ensure the secret video can fit into the carrier video
carrier_capacity = len(carrier_frames) * frame_to_binary_np(carrier_frames[0]).size * 3
secret_size = len(secret_frames) * frame_to_binary_np(secret_frames[0]).size

print(f"Carrier capacity: {carrier_capacity} bits")
print(f"Secret size: {secret_size} bits")

assert secret_size < carrier_capacity, "Secret video is too large to fit in the carrier video."

# Step 2: Embed the secret video
start_time = time.time()
modified_frames = lsb_embed(carrier_frames, secret_frames)
end_time = time.time()
print(f"Embedding secret video took {end_time - start_time:.2f} seconds")

# Step 3: Save the modified video file
start_time = time.time()
save_video(modified_frames, output_video_path, 30)
end_time = time.time()
print(f"Saving modified video took {end_time - start_time:.2f} seconds")

# Step 4: Extract the secret video from the modified video file
start_time = time.time()
extracted_frames = lsb_extract(modified_frames, new_resolution[1], new_resolution[0])
end_time = time.time()
print(f"Extracting secret video took {end_time - start_time:.2f} seconds")

# Save extracted video
start_time = time.time()
save_video(extracted_frames, "extracted_video.avi", 30)
end_time = time.time()
print(f"Saving extracted video took {end_time - start_time:.2f} seconds")
