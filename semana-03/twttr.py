def main():
    word = input("Input: ")
    print(f"Output: {shorten(word)}")

def shorten(word):
    vowel = "aeiou"
    consonants_found = ""
    for letter in word:
        if letter.lower() not in vowel: 
            consonants_found += letter
    return(consonants_found)

if __name__ == "__main__":
    main()