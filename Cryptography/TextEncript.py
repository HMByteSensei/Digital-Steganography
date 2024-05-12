def charSwaper(string, i):
    string_list = list(string)
    for i in range(0, len(string_list) - 1, i):
        string_list[i], string_list[i + 1] = string_list[i + 1], string_list[i]
    return ''.join(string_list)

def charRandomizer(string):
    return charSwaper(charSwaper(charSwaper(string, 2), 3), 5)
def txtEncript(string):
    string = [string[i] for i in range(len(string)-1, -1, -1)]
    result = "".join(string)
    return charRandomizer(result)


s = "Nesto novo"
print(txtEncript(s))
