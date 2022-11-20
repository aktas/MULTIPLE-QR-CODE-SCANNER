import cv2
import pyzbar.pyzbar
import os
import sys
import time
from termcolor import colored
from PIL import Image

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
    -s                Qr code size. Find out with a tool like gimp.
    -T1               Detailed review. It will take long.
    -T2               Default
    -T3               It will be checked quickly.

  Note: Put the pictures you want to scan in the input folder.
  Exp:  python3 qrdecode.py -m1 STMCTF -T3 -s 145
'''
# argparse
mode = None
image_walk = None
qr_size = None
try:
    for arg in sys.argv:
        if arg.lower() == "-d":
            mode = "d"
            print(colored("Default mode is set.","red"))

        if arg.lower() == "-m1":
            mode = "m1"
            ind = sys.argv.index(arg)
            searchValue = sys.argv[ind + 1]
            print(colored("Mode 1 is set.","red"))

        if arg.lower() == "-m2":
            mode = "m2"
            ind = sys.argv.index(arg)
            removeValue = sys.argv[ind + 1]
            print(colored("Mode 2 is set.","red"))

        if arg.lower() == "-h":
            print(colored(help_info, "green"))
            sys.exit()

        if arg.lower() == "-t1":
            image_walk = 10
            print(colored("Detailed review activated. This process may take time.", "red"))

        if arg.lower() == "-t2":
            image_walk = 20
            print(colored("Default review activated.", "red"))

        if arg.lower() == "-s":
            ind = sys.argv.index(arg)
            qr_size = int(sys.argv[ind + 1])
            print(colored("The qr code size is set to {}.".format(qr_size),"red"))

        if arg.lower() == "-t3":
            image_walk = 30
            print(colored("Quick review activated. It will be checked quickly", "red"))


    if qr_size == None:
        print(colored("QR code size must be entered!!!.", "red"))
        sys.exit()

    if mode == None:
        print(colored("Default mode is set.","red"))
        mode = "d"

    if image_walk == None:
        image_walk = 20
        print(colored("Default review activated.", "red"))


except SystemExit:
    sys.exit()
except:
    print(colored("Default mode is set.","red"))
    mode = "d"

time.sleep(3)

print(colored("Images are cropping...","green"))
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
        #image = cv2.imread('input/'+qrImage)
        img = Image.open('input/'+qrImage)
        w, h = img.size

        i = 1
        for walk_h in range(0, h, image_walk):

            for walk_w in range(0, w, image_walk):

                cropped = img.crop((walk_w, walk_h, walk_w+qr_size, walk_h+qr_size))

                cropped.save("output/"+str(i)+".png", "png")
                i += 1

        dosyalar = os.listdir("output/")
        for qrImage in dosyalar:
            if (qrImage.lower().find("png") > -1):
                pass
            else:
                dosyalar.remove(qrImage)
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
    orgImage = orgImage + 1
