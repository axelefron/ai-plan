def main():
    vowel_cutter()

def vowel_cutter():
    vowel = "aeiou"
    word = input("Input: ")
    consonants_found = ""
    for letter in word:
        if letter.lower() not in vowel: 
            consonants_found += letter
    print("Output:",consonants_found)


main()