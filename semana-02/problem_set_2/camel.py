def main():
    word = input("Enter your variable here in camelCase:")
    convert_to_snake(word)
    

def convert_to_snake(word): 
    word_count = ""
    for letter in word:
        if letter.isupper():
            word_count += "_" + letter
        else: 
            word_count += letter

    print("Here's your variable in snake_case:" + word_count.lower())    
        

main()