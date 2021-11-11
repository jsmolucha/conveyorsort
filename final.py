# --- imports ---
from operator import pos
from typing import Counter, Match
import numpy as np
import tkinter as tk
from tkmacosx import Button
import random
import time

# ---TODO---
# [ ]need to make sure the function can restart
# [x]need to incorporate CLS function to clear the status screen after restarting the startLoop()
# [x]create a random generator for the zipcodes on the conveyor belt
# [x]set constraints for the gates according to what zipcode they can accept
# [x]display the output of the zipcodes to the status screen
# [ ] need to fix the stop button so it resets properly 

root = tk.Tk()

root.geometry('700x500')

# --- global variable declarations --- 
colorOn = 'green'
colorOff = 'red'
gates = []
pkgs = []
running  = True
counter = 0
global_counter = 0
pkg = 0

# --- functions ---    
def reset():
    print('timing reset')
    running = True
    status.delete(0, tk.END)

def stopLoop():
    global running
    running = False

    print("attempt_stop")
    status.insert(0, "--- stopped ---")
    start.config(bg = colorOff)

class package:
    def __init__(self, zipcode, serialnum, inserted, position, gate):
        self.zip = zipcode
        self.serial = serialnum
        self.ins = inserted
        self.reqpos = position
        self.g = gate

def startS():
    if running:
        root.after(1000, startS)

    global counter
    global global_counter
    global pkg
    start.config(bg = colorOn)
    global_counter += 10
    counter +=1
    pos = counter * 10
    abs_pos = pos + counter
    timer.insert(counter, pos)
    if counter % 10 == 0:
        timer.delete(0, tk.END)


    #initialize sorting algorithm for every package, every second
    gateSort(global_counter)
    if counter % 10 == 0:
        pkg +=1
        zipcode = random.randint(10000,59999)
        randserial = random.randint(0, 300)
        n = len(pkgs)
        
        pkgs.append(package(zipcode, randserial, counter, abs_pos, pkgSort(zipcode)))
        print('done')
        status.insert(pkg, "serial: {}, zipcode: {}, ins @ {}, reqPos {}, gate {}".format(pkgs[pkg -1].serial, pkgs[pkg -1].zip, pkgs[pkg-1].ins, pkgs[pkg-1].reqpos, pkgs[pkg-1].g))
        print(pkgs[pkg-1].reqpos)
    print(pos)
    print("global time: ", global_counter)

def gateSort(curr):
    n = len(pkgs)
    for i in range(n):
        if pkgs[i].reqpos == curr:
            status.insert(i, "gate {} opened, pkg {} removed @ {} secs".format(pkgs[i].g, pkgs[i].serial, curr))
            gates[pkgs[i - 1].g].config(bg = colorOn)
            root.after(200, lambda: gates[pkgs[i - 1].g].config(bg = colorOff))
            print("ok", pkgs[i].g)

def pkgSort(zipcode):
    gatenum = 0

    if zipcode >= 10000 and zipcode <= 19999:
        gatenum = 0
        
    elif zipcode >= 20000 and zipcode <= 29999:
        gatenum = 1
    
    elif zipcode >=30000 and zipcode <= 39999:
        gatenum = 2

    elif zipcode >=40000 and zipcode <= 49999:
        gatenum = 3

    elif zipcode >=50000 and zipcode <= 59999:
        gatenum = 4

    return gatenum

def writing():
    outF = open('output.txt', 'a')
    outF.write("zipcode {}, gate {} opened".format(zipcode, gatenum + 1, counter))
    outF.write("\n")
    outF.close()
    
for i in range (0,5):
    gates.append(tk.Entry(root, bg='red', width=5,))
    gates[i].pack(side=tk.LEFT)

bottom = tk.Frame(root)
bottom.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

statusLabel = tk.Label(text='Status').pack()
status = tk.Listbox(root, width=40)
status.pack()

counterLabel = tk.Label(text='Timer').pack()
timer = tk.Listbox(root, width=20)
timer.pack()

start = Button(root, bg= 'red', fg='white', text='Start', command=startS)
start.pack(in_=bottom, side=tk.LEFT, fill=tk.BOTH, expand=True)
stop = Button(root, text='Stop', bg='red', fg='white', command=stopLoop)
stop.pack(in_=bottom, side=tk.LEFT, fill=tk.BOTH, expand=True)
terminate = Button(root, text='Terminate', command=root.destroy).pack(in_=bottom, side=tk.LEFT, fill=tk.BOTH, expand=True)

root.mainloop()



"""
    gatenum = int
    n = len(pkgs)
    global counter
    zipcode = random.randint(10000,59999)
    start.config(bg = colorOn)

    if running:
        root.after(1000,startLoop)

    counter += 10
    pkgs.append(zipcode)
    print("rand zip: ", zipcode, counter)
    strng = 'zipcode: {} -> gate{} -> {} secs'.format(zipcode, gatenum + 1, counter)
    status.insert(n, strng)
 """