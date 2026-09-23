import sys

from PIL import Image

images = []

for arg in sys.argv[1:]: # everything except the first index, which is the name program
    image = Image.open(arg)
    images.append(image)

images[0].save("costumes.gif", save_all=True, append_images=[images[1]], duration=200, loop=0)

# this is to create an aniimated gif with the pillow library. you have to download 2 images and with the
# command line arguments calling the images i am looping infinetly si that is creates a moving image or GIF