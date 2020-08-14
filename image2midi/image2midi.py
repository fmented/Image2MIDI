import cv2
import numpy as np
import random
from os import sys
from midiutil import  MIDIFile

def makemidi(img, midi, lo=74, hi=110):
    if int(lo) > 0:
        lo=0
    if int(hi) < 127:
        hi=127

    filename = img
    if filename.endswith('.png'):
        a= cv2.imread(filename, cv2.IMREAD_UNCHANGED)

        trans=a[:,:,3]==0
        a[trans]= [255,255,255,255]

        a=cv2.cvtColor(a, cv2.COLOR_BGRA2BGR)
    else:
        a= cv2.imread(filename, cv2.IMREAD_UNCHANGED)


    h, w = a.shape[:2]

    scale=w/h

    w=int(127*scale)

    dim= (w, 127)
    res= cv2.resize( a, dim, interpolation=cv2.INTER_AREA)

    gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
    (tresh, newimg) = cv2.threshold(gray, 127, 225, cv2.THRESH_BINARY)
    # cv2.imshow('jjj', newimg)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    color = 0
    pixels1=np.argwhere(newimg == 0)
    pixels2=np.argwhere(newimg == 225)

    if pixels1.shape > pixels2.shape:
        pixels= pixels2
    else:
        pixels= pixels1

    

    MyMIDI = MIDIFile(4)  # One track, defaults to format 1 (tempo track is created
                        # automatically)
    MyMIDI.addTempo(0, 0, 180*scale)
    MyMIDI.addProgramChange(0,0,0,0)
    for note, step in pixels:
            MyMIDI.addNote(0, 0, 127-note+1, step, 1, random.randint(int(lo),int(hi)) )


    with open(midi, "wb") as output_file:
        MyMIDI.writeFile(output_file)
    exit("write {} successful".format(midi))


if __name__ == '__main__':
    try:
        prefix = 0 if hasattr(sys, 'real_prefix') else 1
        i = sys.argv[0+prefix]
        o = sys.argv[1+prefix]
        if len(sys.argv)>2+prefix:
            lo = int(sys.argv[2+prefix])
            hi = int(sys.argv[3+prefix])
            makemidi(i, o, lo, hi)
        makemidi(i,o)
    except AttributeError:
        exit('File not found or not an image')
    except IndexError:
        exit("Parameter Error")