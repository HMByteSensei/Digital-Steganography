class TextTransformer:
    def __init__(self):
        pass

    def char_swaper(self, string, step):
        string_list = list(string)
        for i in range(0, len(string_list) - 1, step):
            string_list[i], string_list[i + 1] = string_list[i + 1], string_list[i]
        return ''.join(string_list)

    def rotate_encrypt(self, text):
        result = ''
        for char in text:
            if char.isalpha():
                shifted = ord(char) + 18
                if char.islower():
                    if shifted > ord('z'):
                        shifted -= 26
                elif char.isupper():
                    if shifted > ord('Z'):
                        shifted -= 26
                result += chr(shifted)
            else:
                result += char
        return result

    def rotate_decrypt(self, text):
        result = ''
        for char in text:
            if char.isalpha():
                shifted = ord(char) - 18
                if char.islower():
                    if shifted < ord('a'):
                        shifted += 26
                elif char.isupper():
                    if shifted < ord('A'):
                        shifted += 26
                result += chr(shifted)
            else:
                result += char
        return result

    def char_randomizer(self, string):
        result = self.char_swaper(self.char_swaper(self.char_swaper(string, 2), 3), 5)
        return result

    def txt_encrypt(self, string):
        reversed_string = string[::-1]
        encrypted_string = self.rotate_encrypt(reversed_string)
        randomized_string = self.char_randomizer(encrypted_string)
        return randomized_string

    def txt_decrypt(self, string):
        decrypted_s = self.rotate_decrypt(string)
        unrandomized_string = self.char_swaper(self.char_swaper(self.char_swaper(decrypted_s, 5), 3), 2)
        original = unrandomized_string[::-1]
        return original