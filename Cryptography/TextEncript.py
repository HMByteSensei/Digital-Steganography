def charSwaper(string, i):
    string_list = list(string)
    for i in range(0, len(string_list) - 1, i):
        string_list[i], string_list[i + 1] = string_list[i + 1], string_list[i]
    return ''.join(string_list)

def rotateEncrypt(text):
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

def rotateDecrypt(text):
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
def charRandomizer(string):
    result = charSwaper(charSwaper(charSwaper(string, 2), 3), 5)
    result = charSwaper(charSwaper(charSwaper(result, 2), 3), 5)
    result = charSwaper(charSwaper(charSwaper(result, 2), 3), 5)
    return result

def txtEncript(string):
    string = [string[i] for i in range(len(string)-1, -1, -1)]
    result = "".join(string)
    result = rotateEncrypt(result)
    return charRandomizer(result)


s = "Nesto novo"
print(txtEncript(s))
