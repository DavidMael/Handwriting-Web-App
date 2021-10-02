from PIL import Image
from math import floor

#assumes image only contains nonwhite text on white background

def textDetect(imagepath):
    imagefile = Image.open(imagepath)
    imageRGB = imagefile.convert('RGB')
    image = imageRGB.load()
    width, height = imagefile.size

    lineTop = None
    linebounds = []

    borderWidth = 5

    for scanline in range(borderWidth, height-(borderWidth), 1):

        writingDetected = False

        for pixel in range(borderWidth, width-borderWidth, 1):

            if image[pixel, scanline] != (255, 255, 255):

                writingDetected = True

                #find top of text line
                if lineTop == None:
                    lineTop = scanline

        if writingDetected == False and lineTop != None:

            #only keep elements that have a height of 2.5% of the screen height (about 45 px on my screen)
            if( (scanline - lineTop)/height > 0.025):

                linebounds.append((lineTop, scanline))

            lineTop = None

    return linebounds

#return the number of characters
def charSegment(imagepath, linebounds):

    #print(linebounds)
    #print(len(linebounds))

    imagefile = Image.open(imagepath)
    imageRGB = imagefile.convert('RGB')
    image = imageRGB.load()
    width, height = imagefile.size

    charLeft = None

    counters = []
    imageCtr = 0

    borderWidth = 5

    for line in range(len(linebounds)):

        for column in range(borderWidth, width-borderWidth, 1):

            charDetected = False

            for pixel in range( linebounds[line][0] , linebounds[line][1] , 1 ):

                if image[column, pixel] != (255, 255, 255):

                    charDetected = True

                    if charLeft == None:
                        charLeft = column
                        
            if charDetected == False and charLeft != None:

                characterTop = None
                characterBottom = None
                for row in range (linebounds[line][0] , linebounds[line][1] , 1):
                    blankRow = True
                    for c in range (charLeft, column, 1):
                        if image[c, row] != (255, 255, 255):
                            blankRow = False
                            if characterTop == None:
                                characterTop = row
                    if blankRow == True and characterBottom == None and characterTop != None:
                        characterBottom = row
                if characterBottom == None:
                    characterBottom = linebounds[line][1]

                
                cropped = imagefile.crop((charLeft, characterTop, column, characterBottom))
                if characterBottom - characterTop > column - charLeft:
                    resizedW = floor((column - charLeft)*25/(characterBottom - characterTop))
                    resizedH = 25
                else:
                    resizedW = 25
                    resizedH = floor((characterBottom - characterTop)*25/(column - charLeft))
                resized = cropped.resize(( resizedW , resizedH))
                blank = Image.new('RGB', (28, 28), (255, 255, 255))
                blank.paste(resized, (14 - floor(resizedW/2), 14 - floor(resizedH/2) ))
                try:
                    blank.save( ('character-images/'+str(imageCtr)+'.png'), 'png')
                except AttributeError:
                    print("error saving character image")

                imageCtr = imageCtr + 1

                charLeft = None

        counters.append(imageCtr)

    return counters