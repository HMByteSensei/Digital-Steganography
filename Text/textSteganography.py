from Cryptography.TextCrypto import TextTransformer
class textSteganography:
    def __init__(self):
        pass

    def contains_ordered_letters(self, content, text):
        if(len(text) > len(content)):
            return False
        cleaned_content = ''.join(c.lower() for c in content if c.isalpha())
        cleaned_text = ''.join(c.lower() for c in text if c.isalpha())

        content_ptr, text_ptr = 0, 0
        while content_ptr < len(cleaned_content) and text_ptr < len(cleaned_text):
            if cleaned_content[content_ptr] == cleaned_text[text_ptr]:
                text_ptr += 1
            content_ptr += 1

        return text_ptr == len(cleaned_text)

    def markingLetters(self, content, text):
        # First we removing all of the non-alpha characters
        cleaned_text = ''.join(c for c in text if c.isalpha())
        result = ""

        # pointers for both strings
        content_ptr, text_ptr = 0, 0
        while content_ptr < len(content) and text_ptr < len(cleaned_text):
            if content[content_ptr].lower() == cleaned_text[text_ptr].lower():
                # Match found, underscore the letter; we mark them with underscore in front of letter that we care about(makes secret message)
                result += "_"
                text_ptr += 1
            result += content[content_ptr]
            content_ptr += 1

        # append all remaining characters
        result += content[content_ptr:]
        return result


    def uppercaseLetters(self, content, text):
        # Similar as above
        cleaned_text = ''.join(c for c in text if c.isalpha())

        result = ""
        content_ptr, text_ptr = 0, 0
        while content_ptr < len(content) and text_ptr < len(cleaned_text):
            if content[content_ptr].lower() == cleaned_text[text_ptr].lower():
                # In this case we uppercase all the letters we care about
                result += content[content_ptr].upper()
                text_ptr += 1
            else:
                # and we keep other letters as lowercase
                result += content[content_ptr].lower()
            content_ptr += 1

        result += content[content_ptr:]
        return result

    def uppercaseBinaryLetters(self, content, text):
        # Remove non-alphabetic characters and convert to lowercase
        cleaned_text = ''.join(c for c in text if c.isalpha())
        cleaned_content = ''.join(c for c in content if c.isalpha())
        if(len(cleaned_text) * 8 > len(cleaned_content)):
            return False

        # Get the ASCII values for each characte and convert it to binary
        ascii = ['{0:08b}'.format(ord(c)) for c in cleaned_text]
        result = ""
        content_ptr, ascii_len = 0, 0
        while ascii_len < len(ascii):
            while content_ptr < len(content):
                ascii_ptr = 0
                while ascii_ptr < len(ascii[ascii_len]):
                    if content[content_ptr].isalpha():
                        if ascii[ascii_len][ascii_ptr] == "1":
                            # print (result)
                            result += content[content_ptr].upper()
                        else:
                            result += content[content_ptr].lower()
                        ascii_ptr += 1
                    else:
                        result += content[content_ptr]
                    content_ptr += 1
                break
            ascii_len += 1
        result += content[content_ptr:]
        # print(result)
        return result

    def reverseUppercaseBinaryLetters(self, content):
        content = ''.join(c for c in content if c.isalpha())
        ascii = []
        content_ptr = 0
        while content_ptr < len(content):
            result = ""
            ascii_ptr = 0
            while ascii_ptr < 8:
                if content_ptr >= len(content):
                    break
                if content[content_ptr] == content[content_ptr].upper():
                    result += "1"
                else:
                    result += "0"
                ascii_ptr += 1
                content_ptr += 1
            ascii.append(result)
        ints = []
        for binary in ascii:
            integer_value = int(binary, 2)
            if (integer_value >= 97 and integer_value <= 122) or (integer_value >= 65 and integer_value <= 90):
                ints.append(integer_value)
        result = "".join(chr(i) for i in ints)
        return result

    def reverseMarkingLetters(self, content):
        result = ""
        # pointers for both strings
        content_ptr = 0
        while content_ptr < len(content):
            if content[content_ptr] == "_" and content_ptr + 1 < len(content):
                result += content[content_ptr + 1]
                content_ptr += 1
            content_ptr += 1
        return result

    def reverseUppercaseLetters(self, content):
        content = ''.join(c for c in content if c.isalpha())
        result = ""
        content_ptr = 0
        while content_ptr < len(content):
            if content[content_ptr] == content[content_ptr].upper():
                result += content[content_ptr].upper()
            content_ptr += 1

        return result

    def engine(self, filename, text, method, to_crypt):
        result = ""
        reverse = False
        textTransform = TextTransformer()
        # print("--------TXT-------")
        # print(text)
        # print("--------TXT-------")
        # text = textTransform.txt_encrypt(text)
        # print(text)
        # print(textTransform.txt_decrypt(text))
        # print("--------TXT-------")
        if to_crypt is True:
            text = text.upper()
            text = textTransform.rotate_encrypt(text)
        print(text)
        with open(filename + ".txt", "r") as file:
            content = file.read()
            if method == "markingLetters" or method == 0 or method == "uppercaseLetters" or method == 1:
                if self.contains_ordered_letters(content, text):
                    if method == "markingLetters" or method == 0:
                        result = self.markingLetters(content, text)
                    elif method == "uppercaseLetters" or method == 1:
                        result = self.uppercaseLetters(content, text)
                        print(result)
                        print("HERER")
                else:
                    return False
            elif method == "uppercaseBinaryLetters" or method == 2:
                result = self.uppercaseBinaryLetters(content, text)
            elif method == "reverseMarkingLetters" or method == 3:
                result = self.reverseMarkingLetters(content)
                reverse = True
            elif method == "reverseUppercaseLetters" or method == 4:
                result = self.reverseUppercaseLetters(content)
                reverse = True
                # print(result)
            else:
                reverse = True
                result = self.reverseUppercaseBinaryLetters(content)

            if reverse is True and to_crypt is True:
                result = textTransform.rotate_decrypt(result)
        try:
            with open(filename + "Result.txt", 'w') as file:
                file.write(result)
        except:
            return "Cover text is too short or it does not have all letters that are copntained in secret text."
        return result