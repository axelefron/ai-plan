def main():
    plate = input("Plate: ")
    if is_valid(plate):
        print("Valid")
    else:
        print("Invalid")

def is_valid(s):
    if len(s) < 2 or len(s) > 6:
        return False
    if s.isalnum() == False:
        return False
    if s[0:2].isalpha() == False:
        return False

    number_detected = False
    for c in s:
        if c.isdigit():
            if number_detected == False and c == "0":
                return False
            number_detected = True
        else:
            if number_detected == True:
                return False
            
    return True

    
main()