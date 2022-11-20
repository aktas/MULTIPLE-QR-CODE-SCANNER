# MULTIPLE-QR-CODE-SCANNER
Multiple qr code scanner for image

```
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
```
