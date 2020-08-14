import cv2
import numpy as np
import random
from os import sys

major=[0,2,4,7,9]

def get_octave(l, lo, hi):
    final =[]
    multi=0
    for x in l:    
        while x+ (12*multi) < hi:
            g=x + (12*multi) 
            if g > lo:
                final.append(g)
            multi+=1
        multi=0
    return final

def valmap(value, istart, istop, ostart, ostop):
  return ostart + (ostop - ostart) * ((value - istart) / (istop - istart))

def avg(l):
    return sum(l)/len(l)

def snap(l, n):
    return min(l, key=lambda x: abs(x-n))

def pick(l):
    a=random.randint(0,9)
    if a > 5:
        return max(l)
    else:
        return min(l)

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
    res= cv2.resize( a, dim)

    row=[]
    col=[]
    vel=[]
    for i in range(res.shape[1]):
        for j in range(res.shape[0]):
            r=res[j][i]
            
            row.append(int(pick(r)))
        col.append(int(valmap(row[random.randint(0, len(row))], 0, 255, 36, 72)))
        vel.append(int(valmap(row[random.randint(0, len(row))], 0, 255, lo, hi)))
    notes = []

    music_scale=get_octave(major, 0, 127)
    for x in col:
        n=snap(music_scale, x)
        notes.append(n)

    from midiutil import  MIDIFile

    MyMIDI = MIDIFile(1)

    t=random.randint(120, 180)
    MyMIDI.addTempo(0, 0, t*scale)


    for i, (note, velo) in enumerate(zip(notes, vel)):
        try:
            MyMIDI.addNote(0, 0, note, i/2, random.randint(1,2), velo)
        except :
            MyMIDI.addNote(0, 0, note, i/2, 1, velo)


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

