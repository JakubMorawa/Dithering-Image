from PIL import Image
import numpy as np

def getImage():
    inputFile = 'whiteCat.jpg'
    outputFile = 'WhiteCat_Dithered.jpg'
    img = Image.open(inputFile).convert("L")   # convert to grayscale
    width, height = img.size

    pixels = np.array(img, dtype=float)

    for y in range(height):
        for x in range(width):
            
            oldpixel = pixels[y, x]
            newpixel = 255 if oldpixel >= 128 else 0
            
            quant_error = oldpixel - newpixel

            pixels[y, x] = newpixel

            # Floyd–Steinberg error diffusion
            if x + 1 < width:
                pixels[y, x+1] += quant_error * (7/16)

            if y + 1 < height and x > 0:
                pixels[y+1, x-1] += quant_error * (3/16)

            if y + 1 < height:
                pixels[y+1, x] += quant_error * (5/16)

            if y + 1 < height and x + 1 < width:
                pixels[y+1, x+1] += quant_error * (1/16)

    out = np.clip(pixels, 0, 255).astype(np.uint8)

    Image.fromarray(out).save(outputFile)
    print(f"{outputFile} has been created")

def main():
    getImage()

if __name__ == "__main__":
    main()
