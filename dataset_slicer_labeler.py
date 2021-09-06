from PIL import Image

# disabling the limit temporarily
Image.MAX_IMAGE_PIXELS = None

im = Image.open("rawdata/n19w156.tif")

# re-enabling the limit just in case
Image.MAX_IMAGE_PIXELS = 89478485