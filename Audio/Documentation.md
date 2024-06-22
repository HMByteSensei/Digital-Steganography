# Audio Steganography Tool

## User Guide

### Embedding Tab

When you select the embedding functionality in the tool, the following window will appear:

![Embedding Tab UI](https://github.com/HMByteSensei/Steganografija/blob/main/UI%20Pictures/AudioEmbed.png?raw=true)

#### Instructions

1. **Start by Uploading an Audio Cover File:**
   - Click the **"Upload Audio File"** button.
   - Choose the audio file that will serve as your cover.

2. **Select Your Preferred Method:**
   - Use the dropdown menu to select your preferred embedding method:
     - **LSB (Least Significant Bit)**
     - **DFT (Discrete Fourier Transform)**
     - **DCT (Discrete Cosine Transform)**

3. **Encryption Settings:**
   - In the **"Encryption"** section, check the checkbox to enable encryption if desired.

4. **Input Your Secret Message:**
   - Enter the secret message you want to embed in the provided text box.

5. **Embed Data:**
   - Click the **"Transform"** button to embed the secret message into the audio file using the selected method.

6. **Playback and Visualization:**
   - Use the **"Play"** button to listen to the audio with embedded data and visualize its signal.

7. **Download Embedded Audio:**
   - Click the **"Download"** button to save the modified audio file with embedded data.

### Extract or Detect Tab

When you select the extraction and detection functionality in the tool, the following window will appear:

![Extract and Detect Tab UI](https://github.com/HMByteSensei/Steganografija/blob/main/UI%20Pictures/AudioExtract.png?raw=true)

#### Instructions

1. **Upload Audio File for Extraction or Detection:**
   - Click the **"Upload Audio File"** button.
   - Choose the audio file from which you want to extract or detect data.

2. **Select Your Preferred Method:**
   - Use the dropdown menu to select your preferred extraction method:
     - **LSB (Least Significant Bit)**
     - **DFT (Discrete Fourier Transform)**
     - **DCT (Discrete Cosine Transform)**

3. **Enter Message Length (for Extraction):**
   - Input the expected length of the secret message if known.

4. **Encryption Settings:**
   - Check the checkbox if encryption was used during embedding.

5. **Extract or Detect Data:**
   - Click the **"Extract"** or **"Detect"** button based on your intention.
     - **Extract:** Retrieve the embedded secret message from the audio file.
     - **Detect:** Determine if a specific word exists in the audio file.

6. **Reset Extraction or Detection:**
   - Click the **"Reset Extraction"** button to clear input fields and selections related to extraction.