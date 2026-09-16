from pyfiglet import Figlet
import random
import sys

figlet = Figlet()
fonts = figlet.getFonts()

if len(sys.argv) == 1:
    font = random.choice(fonts)
elif len(sys.argv) == 3:
    if sys.argv[1] != "-f" and sys.argv[1] != "--font":
        sys.exit("Invalid usage")
    if sys.argv[2] in fonts:
        font = sys.argv[2]
    else:
        sys.exit("Invalid usage")
else:
    sys.exit("Invalid usage")

user_input = input("Input: ")
figlet.setFont(font=font)

print("Output:", figlet.renderText(user_input))

 
