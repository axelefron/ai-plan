def main():
    food_time = input("What time is it?: ")
    time = convert(food_time)

    if 7 <= time <= 8:
        print("Breakfast time")

    elif 12 <= time <= 13:
        print("Lunch time")

    elif 18 <= time <= 19:
        print("Dinner time")
   
def convert(time):
    hours, minutes = time.split(":")
    hours = float(hours)
    minutes = float(minutes) / 60
    return hours + minutes

if __name__ == "__main__":
    main()


