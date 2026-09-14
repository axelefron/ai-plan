def main():
    fraction = get_fraction()
    final_result = round(fraction * 100)

    if final_result >= 99:
        print("F")
    elif final_result <= 1:
        print("E")
    else:
        print(f"{final_result}%")

def get_fraction():
    while True:
        try:
            fraction = input("Enter a fraction here: ").split("/")
            numerator = int(fraction[0])
            denominator = int(fraction[1])
            result = numerator / denominator
            if result > 1:
                continue
        except (ValueError, ZeroDivisionError):
            pass
        else:
            if 0 <= result <= 1:
                return result
        

main()