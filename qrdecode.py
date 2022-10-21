import cv2
import numpy as np
import qrtools
import pyzbar.pyzbar
import os
import sys
import time
from termcolor import colored



# ffmpeg -i qr.gif temp/temp%d.png
print(colored(r"""
 ▄▄▄▄▄▄▄ ▄ ▄▄▄ ▄▄▄▄▄▄▄
 █ ▄▄▄ █ ▄▄▀█  █ ▄▄▄ █
 █ ███ █ █▀ ▄▀ █ ███ █
 █▄▄▄▄▄█ ▄▀█▀█ █▄▄▄▄▄█        MULTIPLE QR CODE SCANNER
 ▄▄▄▄  ▄ ▄▄▄██▄  ▄▄▄ ▄
 ▀▀▄▄██▄▀▄▀▀█▀▀ █ █ █                by aktas
 █▄▀█▄█▄█▄▀ ▀▄▀▀▀ ▀█▀█       https://github.com/aktas
 ▄▄▄▄▄▄▄ ▀▄ █▄  █▄█  █
 █ ▄▄▄ █  █▀ ▄█▄▀▀ ▀██
 █ ███ █ ██▄ ▄▄▀▀█▄▄▀
 █▄▄▄▄▄█ █ ▄▀  ▄▄▄▄ ▄
""","green"))

help_info = '''
  Usage: qrdecoder.py [OPTIONS] [VALUE]
    -d                Default. Prints all output.
    -m1               Mode 1 is used if there is a searched word.
    -m2               Mode 2 is used if there is a word to be removed.

  Note: Put the pictures you want to scan in the input folder.
'''

mode = None
try:
    for arg in sys.argv:
        if arg == "-d":
            mode = "d"
            print(colored("Default mode is set.","red"))
            break
        if arg == "-m1":
            mode = "m1"
            searchValue = sys.argv[2]
            print(colored("Mode 1 is set.","red"))
            break
        if arg == "-m2":
            mode = "m2"
            removeValue = sys.argv[2]
            print(colored("Mode 2 is set.","red"))
            break

        if arg == "-h":
            print(colored(help_info, "green"))
            sys.exit()

    if mode == None:
        print(colored("Default mode is set.","red"))
        mode = "d"
except SystemExit:
    sys.exit()
except:
    print(colored("Default mode is set.","red"))
    mode = "d"

time.sleep(3)

qrImages = os.listdir("input/")
for qrImage in qrImages:
    if (qrImage.lower().find("png") > -1) or (qrImage.lower().find("pneg") > -1) or (qrImage.lower().find("jpg") > -1) or (qrImage.lower().find("jpeg") > -1) or (qrImage.lower().find("jfif") > -1):
        pass
    else:
        qrImages.remove(qrImage)

orgImage = 1
for qrImage in qrImages:
    try:
        files = os.listdir("output/")
        for file in files:
            os.remove("output/"+file)
        image = cv2.imread('input/'+qrImage)
        original = image.copy()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (9,9), 0)
        thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        # Morph close
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
        close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)

        # Find contours and filter for QR code
        cnts = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        i = 0
        for c in cnts:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.04 * peri, True)
            x,y,w,h = cv2.boundingRect(approx)
            area = cv2.contourArea(c)
            ar = w / float(h)
            if len(approx) > 2 and area > 100 and (ar > .15 and ar < 1.7):
                crop_img = image[y:y+h, x:x+w]
                cv2.imwrite("output/"+str(i)+".jpg", crop_img)
                #cv2.rectangle(image, (x, y), (x + w, y + h), (36,255,12), 3)
                #ROI = original[y:y+h, x:x+w]
                #cv2.imwrite('ROI.png', ROI)
            i = i + 1

        dosyalar = os.listdir("output/")
        for qrImage in dosyalar:
            if (qrImage.lower().find("jpg") > -1):
                pass
            else:
                qrImages.remove(qrImage)
        print(colored("The files of the "+str(orgImage)+"th photo have been saved. Reading qr code!!","green"))
        for file in dosyalar:
            image = cv2.imread("output/"+file)

            decodedObjects = pyzbar.pyzbar.decode(image)
            for obj in decodedObjects:
                #print(obj.data.decode("utf-8"))
                data = obj.data.decode("utf-8")
                if mode == "d":
                    print(obj.data.decode("utf-8"))
                elif mode == "m1":
                    if data.find(searchValue) > -1:
                        print(obj.data.decode("utf-8"))
                        sys.exit()
                    else:
                        pass
                else:
                    if data.find(removeValue) > -1:
                        pass
                    else:
                        print(obj.data.decode("utf-8"))
                        sys.exit()

    except SystemExit:
        sys.exit()
    except:
        pass
    orgImage = orgImage + 1
