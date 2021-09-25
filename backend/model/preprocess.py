from PIL import Image
from math import floor

#assumes image only contains nonwhite text on white background

def textDetect(imagepath):
    imagefile = Image.open(imagepath)
    imageRGB = imagefile.convert('RGB')
    image = imageRGB.load()
    width, height = imagefile.size

    print("dimensions:", width, height)

    lineTop = None
    linebounds = []

    for scanline in range(height):

        writingDetected = False

        for pixel in range(width):

            if image[pixel, scanline] != (255, 255, 255):

                writingDetected = True

                #find top of text line
                if lineTop == None:
                    lineTop = scanline
                    print("top detected at:", scanline)

        if writingDetected == False and lineTop != None:

            print("bottom detected at:", scanline)

            #only keep elements that have a height of 2.5% of the screen height (about 45 px on my screen)
            if( (scanline - lineTop)/height > 0.025):

                for i in range(width):
                    image[i, lineTop] = (255, 0, 0)
                    image[i, scanline] = (0, 255, 0)

                linebounds.append((lineTop, scanline))
            
            else:

                for i in range(width):
                    image[i, lineTop] = (255, 170, 00)
                    image[i, scanline] = (119, 255, 0)


            lineTop = None

    #imageRGB.show()

    return linebounds

def charSegment(imagepath, linebounds):

    print(linebounds)
    print(len(linebounds))

    imagefile = Image.open(imagepath)
    imageRGB = imagefile.convert('RGB')
    image = imageRGB.load()
    width, height = imagefile.size

    charLeft = None

    imageCtr = 0

    for line in range(len(linebounds)):

        for column in range(width):

            charDetected = False

            for pixel in range( linebounds[line][0] , linebounds[line][1] , 1 ):

                if image[column, pixel] != (255, 255, 255):

                    charDetected = True

                    if charLeft == None:
                        charLeft = column
                        
            if charDetected == False and charLeft != None:

                for i in range( linebounds[line][0] , linebounds[line][1] , 1 ):
                    image[charLeft, i] = (255, 0, 0)
                    image[column, i] = (0, 255, 0)

                cropped = imagefile.crop((charLeft, linebounds[line][0], column, linebounds[line][1]))
                if linebounds[line][1] - linebounds[line][0] > column - charLeft:
                    resizedW = floor((column - charLeft)*28/(linebounds[line][1] - linebounds[line][0]))
                    resizedH = 28
                else:
                    resizedW = 28
                    resizedH = floor((linebounds[line][1] - linebounds[line][0])*28/(column - charLeft))
                resized = cropped.resize(( resizedW , resizedH))
                blank = Image.new('RGB', (28, 28), (255, 255, 255))
                #print(14 - floor(resizedW/2))
                blank.paste(resized, (14 - floor(resizedW/2), 14 - floor(resizedH/2) ))
                try:
                    blank.save( ('character-images/'+str(imageCtr)+'.png'), 'png')
                except AttributeError:
                    print("error saving character image")

                imageCtr = imageCtr + 1

                charLeft = None
 
    #imageRGB.show()