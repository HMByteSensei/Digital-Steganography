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
        if(len(text) * 8 > len(content)):
            return False
        # Remove non-alphabetic characters and convert to lowercase
        cleaned_text = ''.join(c for c in text if c.isalpha())

        # Get the ASCII values for each characte and convert it to binary
        ascii = ['{0:08b}'.format(ord(c)) for c in cleaned_text]
        result = ""
        content_ptr, ascii_ptr, ascii_len = 0, 0, 0
        while  ascii_len < len(ascii):
            for (char, bin) in zip(content, ascii[ascii_len]):
                if bin == "1":
                    result += char.upper()
                else:
                    result += char.lower()
            ascii_len += 1
        return result

    def engine(self, filename, text, method):
        result = ""
        t = TextTransformer()
        text = t.txt_encrypt(text)
        with open(filename + ".txt", "r") as file:
            content = file.read()
            if method == "markingLetters" or method == 0 or method == "uppercaseLetters" or method == 1:
                if(self.contains_ordered_letters(content, text)):
                    if method == "markingLetters" or method == 0:
                        result = self.markingLetters(content, text)
                    elif method == "uppercaseLetters" or method == 1:
                        result = self.uppercaseLetters(content, text)

        return result
