
from PIL import Image, ImageDraw
import math

reference = "your.jpg"
imageSize = (1000, 1000)
imageSize1 = 1000
nails = 200
notAgain = []

nailsD = {}
ddPixel = {}
pixelList = []

image = Image.open(reference)

def imageToSquare(img): #image centered tried to be fancy may just overcomplicated it but I think its elligant
    
    size = img.size
    w, h = size

    start = (max(size) - min(size))/2
    end =   start + min(size)

    if w > h:
        img = img.crop((start, 0, end, h))
    else:
        img = img.crop((0, start, w, end))

    img = img.resize(imageSize)
    img = img.convert("L")
    #img.show()
    return (img)

def imageCircle (img): #create a mask over the image of a circle (does nothing but makes it easier to see also better when looking at pixel values though might skew we'll see)

    w , h = img.size
    mask = Image.new('L',img.size,0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0,0,w,h), fill = 255 )

    circleImg = Image.new('L',img.size)
    circleImg.paste(img,mask = mask)
    circleImg.save("TrueReference.jpg")

    #circleImg.show()
    return circleImg

def nailPlacement(): #determines pixel placement of the nails arcosss the circle
    nailPlaced = {}

    for i in range(nails):
        x = imageSize1/2 * math.cos(2*math.pi * i / nails) + 500
        y = imageSize1/2 * math.sin(2*math.pi * i / nails) + 500

        nailPlaced[i] = int(x), int(y) 

    return nailPlaced

def pixels (): #creates a list of all the pixels values
    pixels = list(img.getdata())
    return pixels
    
def pixelConverter (): #changes picture to rgb (probably not useful)
    img = Image.new("RGB", (imageSize))
    img.putdata(pixels())
    img.show()
    
def lineFinder(startNail): #finds the darkest line from a given point to the rest of the nails
    dark0 = []
    dark1 = [0]
    
    bestNail = 0
    
    for i in range(nails):
        
        cordsList = bresenhan (nailsD[startNail], nailsD[i])
        tempDark = []

        conNails = (startNail,i)

        for cords in cordsList:  #edits list to add all cords values for one line
            x, y = cords
            dark0.append(ddPixel[x][y])
        
        tempDark = dark0 #temp storage
        dark0 = []

        if (startNail,i) not in notAgain and sum(tempDark) / len(tempDark) > sum(dark1) / len(dark1): #hopefully avg darkness over the line of the picture compares it to see which is the best connection

            dark1 = tempDark
            bestNail = i
    
    conNails = (startNail,bestNail)

    return (conNails)

def nestPixels (): # creates a *double* dictionary where the cords can be found like rows and colums
    ddPixelf = {}
    dPixel = {}

    for i in range(1001):
        for j in range(1001):
            dPixel[j] = pixelList[i+j]
        ddPixelf[i] = dPixel
    return ddPixelf

def bresenhan (pointA, pointB): # bresenhan line algo, finds cords along a line from (x1,y1) to (x2,y2)
    x0, y0 = pointA
    x1, y1 = pointB

    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = -1 if x0 > x1 else 1
    sy = -1 if y0 > y1 else 1
    err = dx - dy

    coOrdinates = []

    while x0 != x1 or y0 != y1:
        coOrdinates.append((x0, y0))

        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy

    coOrdinates.append((x1, y1))

    #print(coOrdinates)
    return coOrdinates
    
def drawLines(strings):
    
    img = Image.new("RGB", (imageSize))
    img.putdata(pixelList)
    draw = ImageDraw.Draw(img)

    start = 0

    for i in range (strings):
        startPoint, endPoint = lineFinder(start)
        
        #print(startPoint, endPoint)
        #print(nailsD[startPoint], nailsD[endPoint])
        draw.line([ nailsD[startPoint], nailsD[endPoint] ],fill = (0,0,255), width = 1)
        
        notAgain.append((startPoint,endPoint))
        if startPoint != endPoint:
            notAgain.append((endPoint, startPoint))

        start = endPoint
    img.show()

img = imageCircle(imageToSquare(image))

nailsD =  nailPlacement()
pixelList = pixels()
ddPixel = nestPixels()



drawLines(1000)

#ddPixelTester()

#print(nestPixels())
#print(bresenhan((0,0),(500,500)))

#print(nailPlacement(nails,imageSize))
#pixelTester(pixels(imageCircle(imageToSquare(image(reference),imageSize))))
#imageToSquare(image(reference))
    
    