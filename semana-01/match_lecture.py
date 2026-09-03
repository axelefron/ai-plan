name = input("What is your name?: ").strip().title()

match name:
    case "Axel" | "Tiago": # el "|" se usa como un OR. Separas valores que entran en la misma categoria para no tener que crear otro case
        print("Boca Juniors")
    case "Nico":
        print("Velez Sarfield")
    case "Kike":
        print("Valencia F.C")
    case "Luru":
        print("Real Madrid")
    case _: # --> el simbolo "_" se usa para asignar todo el resto de valores, seria ocmo un else. si el usuario no pone un nombre que este en los valores asignados de algun case, usando el "_" queda asignado en su nuevo case
        print("Who?")

