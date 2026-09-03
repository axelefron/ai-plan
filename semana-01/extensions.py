file_type = input("Enter your file name here: ").strip().casefold()

if file_type.endswith(".gif"):
    print("image/gif")

elif file_type.endswith(".jpg") or file_type.endswith(".jpeg"):
    print("image/jpeg")

elif file_type.endswith(".png"):
    print("image/png")

elif file_type.endswith(".pdf"):
    print("application/pdf")

elif file_type.endswith(".txt"):
    print("text/plain")

elif file_type.endswith(".zip"):
    print("application/zip")

else:
    print("application/octet-stream")

"""
ESTA SERIA LA VERSION MEJORADA O USANDO MATCH, (LA MAS PYTHONICA ES CON DICCIONARIOS PERO LO VEO MAS ADELANTE)

file_name = input("Enter your file name here: ").strip().casefold()
extension = file_name.split(".")[-1]

match extension:
    case "gif":
        print("image/gif")
    case "jpg" | "jpeg":
        print("image/jpeg")
    case "png":
        print("image/png")
    case "pdf":
        print("application/pdf")
    case "txt":
        print("text/plain")
    case "zip":
        print("application/zip")
    case _:
        print("application/octet-stream")
"""