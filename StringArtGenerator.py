from PIL import Image, ImageDraw, ImageTk
import math
import random
import turtle
import tkinter as tk


reference = "storm.jpg"  # the image used
nails = 300 #doesn't do much but sets amount of nails across the circle
strings = 900 #the higher the darker image will appear and usually above 500 too slow and less impact
minStringLength = 550  #greatly affects results

references = {0:"storm.jpg",1:"smiley.jpg",2:"Rosen.jpg",3:"your.jpg",4:"testCircle.tif",
              5:"Bertram.jpg",6:"nuhuh.png",7:"fun.png",8:"jamesTest.png",9:"Daub.jpg",
              10:"davis.jpg"}

#don't change
imageSize = (1000, 1000)
imageSize1 = 1000
image = Image.open(reference)

notAgain = []
nailsD = {}
nailsT = {}
ddPixel = {}
pixelList = []

nailsToConnect = []

randomOn = False

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

    return (img)

def imageCircle (img): #create a mask over the image of a circle (does nothing but makes it easier to see also better when looking at pixel values though might skew we'll see)

    w , h = img.size
    mask = Image.new('L',img.size,0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0,0,w,h), fill = 255 )

    circleImg = Image.new('L',img.size)
    circleImg.paste(img,mask = mask)
    circleImg.save("TrueReference.jpg")

    return circleImg

def nailPlacement(): #determines pixel placement of the nails arcosss the circle
    nailPlaced = {}
    nailPlacedT = {}

    for i in range(nails):
        x = max(0, min (imageSize1/2 * math.cos(2*math.pi * i / nails) + imageSize1/2,imageSize1-1))
        y = max(0, min (imageSize1/2 * math.sin(2*math.pi * i / nails) + imageSize1/2,imageSize1-1))

        xt = imageSize1/2 * math.cos(2*math.pi * i / nails) 
        yt = imageSize1/2 * math.sin(2*math.pi * i / nails)        

        nailPlacedT[i] = (xt), (yt) 
        nailPlaced[i] = int(x), int(y) 

    return nailPlaced, nailPlacedT

def pixels (): #creates a list of all the pixels values
    pixels = list(img.getdata())
    return pixels
    
def lineFinder(startNail): #finds the darkest line from a given point to the rest of the nails
    dark0 = []
    dark1 = [255]
    
    bestNail = startNail + 1
    if bestNail >= nails:
        bestNail -= nails
    
    for i in range(nails):
        
        cordsList = bresenhan (nailsD[startNail], nailsD[i])
        tempDark = []

        conNails = (startNail,i)

        for cords in cordsList:  #edits list to add all cords values for one line
            x, y = cords
            dark0.append(ddPixel[y][x])
        
        tempDark = dark0 #temp storage
        dark0 = []

        #hopefully avg darkness over the line of the picture compares it to see which is the best connection 
        #also makes sure the stringLength is long enough so there isn't (as much) clumping towards darker regions
        #also removes the possibility of going over those two nails again
        if len(tempDark) > minStringLength and (startNail,i) not in notAgain and (sum(tempDark) / len(tempDark)) < (sum(dark1) / len(dark1)): 
            dark1 = tempDark
            bestNail = i
    
    conNails = (startNail,bestNail)

    return (conNails)

def nestPixels (): # creates a *double* dictionary where the cords can be found like rows and colums
    ddPixelf = {}
    dPixel = {}

    pixelCount = 0

    for i in range(imageSize1):
        for j in range(imageSize1):
            dPixel[j] = pixelList[pixelCount]
            pixelCount += 1
        ddPixelf[i] = dPixel
        dPixel = {}
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
    #print(nails,strings,minStringLength)

    img = Image.new("RGBA", (imageSize), "white")
    #img.putdata(pixelList)
    draw = ImageDraw.Draw(img)

    start = 0
    
    screen = turtle.Screen()
    screen.screensize(imageSize1,imageSize1)
    screen.tracer(0)

    t = turtle.Turtle()
    t.speed(0)
    t.up()

    for i in range (strings):
        startPoint, endPoint = lineFinder(start)
        
        x0 , y0 = nailsT[startPoint]
        x1 , y1 = nailsT[endPoint]

        draw.line([ nailsD[startPoint], nailsD[endPoint] ],fill = (120,120,120,60), width = 1)
        t.goto(x0,y0 * -1)
        t.down()
        t.goto(x1,y1 * -1)
        t.up()
        
        screen.update()

        notAgain.append((startPoint,endPoint))
        if startPoint != endPoint:
            notAgain.append((endPoint, startPoint))
        
        nailsToConnect.append((startPoint,endPoint))
        
        '''eather one works fine random probably better but the incrementation looks nice when the picture is developing'''
        if randomOn:
            start = random.randint(0,nails-1)
        else:
            start += 1
            if start >= nails:
                start -= nails

    img.show()
    img.save("endProduct.png")
    turtle.done

    return img

def updateImageD(imageN): #updates Image used
    index = int(imageN)
    imageTKO = references.get(index,"blank")
    labelImage.config(text=f"{imageTKO}")
    
    currentDisplay = Image.open(references[index])
    wTK, hTK = currentDisplay.size
    scaler = 250/hTK #scales the image down to at least 250 just to look nice
    currentD = currentDisplay.resize((int(wTK*scaler), int(hTK*scaler))) 
    new_image = ImageTk.PhotoImage(currentD)
    imageLabel.config(image=new_image)
    imageLabel.image = new_image 

    global image
    image = currentDisplay

def updateNails(aNail): #updates global variable nails
    labelNails.config(text=f"Amount of Nails: {aNail}")
    global nails
    nails = int(aNail)

def updateStrings(aString): #updates global variable strings
    labelString.config(text=f"Amount of String(s): {aString}")
    global strings
    strings = int(aString)

def updateStringLength(lString): #updates global variable minStringLength
    labelStringL.config(text=f"Min Length of String(s): {lString}% Image Size")
    global minStringLength 
    minStringLength = int(lString)/100 * imageSize1

def updatImageSize(imgSize): #updates global variable imageSize
    labelimageSize.config(text=f"Size of Image: {imgSize}")
    global imageSize, imageSize1 
    imageSize1 = int(imgSize)
    imageSize = int(imgSize), int(imgSize)

root = tk.Tk() #creates the gui screen
root.title("String Art Settings")

imaget = Image.open(references[0]) 
widthTK, heightTK = imaget.size
scalerD = 250/heightTK
imageTK = imaget.resize((int(widthTK*scalerD),int(heightTK*scalerD)))

imageTK = ImageTk.PhotoImage(imageTK)

imageLabel = tk.Label(root, image=imageTK)
imageLabel.pack()

#image selection
imageSlider = tk.Scale(root, from_=0, to=len(references)-1, orient=tk.HORIZONTAL, command=updateImageD, length = 400)
imageSlider.pack(padx=20, pady=5)
labelImage = tk.Label(root, text="storm.jpg")
labelImage.pack(side=tk.TOP, padx=10, pady=5)

#amount of nails slider
nailSlider = tk.Scale(root, from_=50, to=500, orient=tk.HORIZONTAL, command=updateNails, length = 400)
nailSlider.pack(padx=20, pady=5)
labelNails = tk.Label(root, text="Amount of Nails: 50")
labelNails.pack(side=tk.TOP, padx=10, pady=5)
nailSlider.set(150)

#amount of strings slider
stringsSlider = tk.Scale(root, from_=1, to=10000, orient=tk.HORIZONTAL, command=updateStrings, length = 400)
stringsSlider.pack(padx=20, pady=5)
labelString = tk.Label(root, text="Amount of String(s): 1")
labelString.pack(side=tk.TOP, padx=10, pady=5)
stringsSlider.set(1250)

#percent of imageSize for length of min string
stringLSlider = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, command=updateStringLength, length = 400)
stringLSlider.pack(padx=20, pady=5)
labelStringL = tk.Label(root, text="Min Length of String(s): 0% Image Size")
labelStringL.pack(side=tk.TOP, padx=10, pady=5)
stringLSlider.set(10)

#Sets image size
imageSizeSlider = tk.Scale(root, from_=500, to=10000, orient=tk.HORIZONTAL, command=updatImageSize, length = 400)
imageSizeSlider.pack(padx=20, pady=5)
labelimageSize = tk.Label(root, text="Size of Image:0")
labelimageSize.pack(side=tk.TOP, padx=10, pady=5)
imageSizeSlider.set(1000)

#random placement toggle
def toggle():
    global randomOn
    if swv.get():
        randomOn = True
    else:
        randomOn = False

swv = tk.BooleanVar()

switchRan = tk.Checkbutton(root, text="Random Nail Placement", variable=swv, command=toggle)
switchRan.pack(pady=20)

#Start function sets variables that need the variables that were changed in the slider
def commencer():
    global img, nailsD, nailsT, pixelList, ddPixel
    img = imageCircle(imageToSquare(image))
    nailsD , nailsT=  nailPlacement()
    pixelList = pixels()
    ddPixel = nestPixels()
    drawLines(strings)

commence = tk.Button(root, text="COMMENCE", command=lambda: commencer())
commence.pack(pady=20)

root.mainloop()

print(nailsToConnect)

#drawLines(strings)
    
    