def caesar_encrypt(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            if char.isupper():
                result += chr((ord(char) - 65 + shift) % 26 + 65)
            else:
                result += chr((ord(char) - 97 + shift) % 26 + 97)
        else:
            result += char
    return result

def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)

def fence_encrypt(text):
    text = text.replace(" ", "")
    if len(text) <= 1:
        return text
    
    even = ""
    odd = ""
    
    for i in range(len(text)):
        if i % 2 == 0:
            even += text[i]
        else:
            odd += text[i]
    
    return even + odd


def fence_decrypt(text):
    if len(text) <= 1:
        return text
    
    mid = (len(text) + 1) // 2
    even = text[:mid]
    odd = text[mid:]
    
    result = ""
    for i in range(mid):
        result += even[i]
        if i < len(odd):
            result += odd[i]
    
    return result


