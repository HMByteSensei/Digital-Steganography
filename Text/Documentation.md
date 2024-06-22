# Text Steganography Tool

## User Guide
When you select the text steganography technique, the following window will appear:

![image](https://github.com/HMByteSensei/Steganografija/blob/main/UI%20Pictures/Text%20window.png?raw=true)

### Instructions:

1. **Start by Selecting a Cover Text File:**
   - Click the **"Search"** button.
   - Choose the text file that will serve as your cover text.

2. **Select Your Preferred Method:**
   - Use the combo box to select your preferred steganography method.

3. **Encryption Settings:**
   - In the **"Encryption"** section, use the radio buttons to indicate if you want to encrypt the secret message before embedding it into the text file.
     - **True:** Encrypt the secret message.
     - **False:** Do not encrypt the secret message.

4. **Steganography Settings:**
   - In the **"Steganography"** section, use the radio buttons to specify the operation:
     - **Steganography = True:** Hide data in the text file.
     - **Steganography = False:** Extract data from the text file.

5. **Input Your Secret Message:**
   - Enter the secret message you want to hide in the second text box.

6. **Generate the Steganographic Text File:**
   - Click **"Done"** to generate a new text file with the hidden message. The new file will be named as `old_nameResult.txt`.