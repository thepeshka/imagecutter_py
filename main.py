import logging
logging.basicConfig(filename="imagecutterpy.log",level=logging.CRITICAL)
from PIL import Image
from psd_tools import PSDImage
import os
import subprocess
import math
def openImage(srcImgPath):
    extendName = srcImgPath.split(".")[-1].lower()
    changeSubStatus("extendName =",extendName)
    if extendName in ("jpg", "png", "psd"):
        changeSubStatus("opening file...")
        if extendName == "psd":
            im = PSDImage.load(srcImgPath).as_PIL()
        else:
            im = Image.open(srcImgPath)
    return im

def cutImage(im,targetPath,chunksize=512):
    if not os.path.exists(targetPath):
        os.mkdir(targetPath)
    width = im.size[0]
    height = im.size[1]
    maxchuncks = math.ceil(width / chunksize)*math.ceil(height / chunksize)
    chunck = 0
    w = 0
    h = 0
    x = 0
    y = 0
    while w < width - chunksize:
        while h < height - chunksize:
            chunck += 1
            box = (w, h, w + chunksize, h + chunksize)
            changeSubStatus("["+str(int((chunck/maxchuncks)*100))+"%]","["+str(chunck)+"/"+str(maxchuncks)+"]","cropping...")
            result = im.crop(box)
            pngPath = targetPath + "/map_%d_%d.png"%(x,y)
            changeSubStatus("["+str(int((chunck/maxchuncks)*100))+"%]","["+str(chunck)+"/"+str(maxchuncks)+"]","saving...")
            result.save(pngPath)
            cmd = "nvdxt.exe -file %s -output %s -dxt1c"%(pngPath, targetPath + "/map_%d_%d.dds"%(x,y))
            changeSubStatus("["+str(int((chunck/maxchuncks)*100))+"%]","["+str(chunck)+"/"+str(maxchuncks)+"]","converting...",cmd)
            p = subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True)
            (stdoutdata, stderrdata) = p.communicate()
            logging.info(stdoutdata)
            logging.info(stderrdata)
            os.remove(pngPath)
            h += chunksize
            y += 1
        y = 0
        w += chunksize
        x += 1
        h = 0

def resizeImage(im,size):
    im.thumbnail(size, Image.ANTIALIAS)
    return im

def changeMainStatus(*arg):
    text = ""
    for i in arg:
            text = text + str(i) + " "
    print(text)
    logging.info(text)

def changeSubStatus(*arg):
    text = ""
    for i in arg:
            text = text + str(i) + " "
    print(text)
    logging.info(text)

def main(imagepath,targetpath,maxiters,chuncksize):
    if targetpath[-1] not in ["\\","/"]:
        targetpath = targetpath + "\\"
    iterations = maxiters
    im = openImage(imagepath);
    while(iterations > 0):
        changeMainStatus("["+str(maxiters - iterations + 1)+"/"+str(maxiters)+"]","cutting image..")
        cutImage(im,targetpath+str(3-iterations),chuncksize)
        changeMainStatus("["+str(maxiters - iterations + 1)+"/"+str(maxiters)+"]","resizing image...")
        im = resizeImage(im,(im.width/2,im.height/2))
        iterations -= 1
    changeMainStatus("finish")

try:
    from tkinter.filedialog import askopenfilename
    import tkinter as tk

    root = tk.Tk()
    root.withdraw()
    filename = askopenfilename(initialdir = os.getcwd(),title = "Source",filetypes = (("PSD","*.psd"),("JPG","*.jpg"),("PNG","*.png")))
    main(filename,os.getcwd(),3,512)
except Exception as e:
    logging.error("Unhandled exception: "+repr(e))
