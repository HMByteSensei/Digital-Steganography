# Custom Cryptography

## Overview

- The TextTransformer class provides several text manipulation methods, including character swapping, rotation-based encryption and decryption, character randomization, and comprehensive text encryption and decryption. These methods can be used to transform and secure text strings in various ways.


- These methods are part of our own custom encryption scheme, implemented for showcase purposes, demonstrating how various transformations can be combined to secure text strings.

## Main Methods
- txt_encrypt(string)
  - Implementation:
  
  - Reverses the input string.

  - Applies the rotate_encrypt method on the reversed string.

  - Applies the char_randomizer method on the encrypted string.

  - Returns the final encrypted string.

- txt_decrypt(string)
    - Implementation:

  - Applies the rotate_decrypt method on the input string.

  - Reverses the character randomization by calling the char_swaper method with steps of 5, 3, and 2 respectively.

  - Reverses the resulting string to get the original text.

  - Returns the decrypted string.

## Usage Example

```
# Create an instance of TextTransformer
transformer = TextTransformer()

# Original text
original_text = "Example text"

# Encrypt the text
encrypted_text = transformer.txt_encrypt(original_text)
print("Encrypted:", encrypted_text)

# Decrypt the text
decrypted_text = transformer.txt_decrypt(encrypted_text)
print("Decrypted:", decrypted_text)

# Output should show the original text
```