# -*- coding: utf-8 -*-
"""
Created on Fri Aug  4 04:52:13 2017

@author: irvan
"""

import sys
import threading
import signal
import os, glob
from subprocess import check_output
import tkMessageBox
from PIL import ImageTk


if sys.version_info[0] == 2:  # Just checking your Python version to import Tkinter properly.
    from Tkinter import *
    
else:
    from tkinter import *
    
playState = False
pauseState = False
global btnCounter
btnCounter = 0
listvideos = False
from subprocess import check_output
def get_pid(name):
    return map(int,check_output(["pidof",name]).split())
 
class Fullscreen_Window:

    def __init__(self):
        self.tk = Tk()
        self.tk.title("Main Control ver.04")
        self.tk.config(bg="black")
        self.tk.geometry('480x320')
        #self.tk.attributes('-zoomed', True)  # This just maximizes it so we can see the window. It's nothing to do with fullscreen.
        global frame        
        frame = Frame(self.tk,bg="black")
        frame.grid(row=1,column=0)
        global frame2
        frame2 = Frame(self.tk,bg="black")
        frame2.grid(row=0,column=0, sticky=W)
        self.create_widgets()
        self.state = False
        self.toggle_fullscreen(event=False)
        self.tk.bind("<Escape>", self.end_fullscreen)
        self.tk.bind("<F11>", self.toggle_fullscreen)
        
    def play(self):
        global playState
        global pauseState
        global os
        os.system('sudo killall avconv')
        os.system('sh ~/restartpiwall.sh')
                
        while playState == True:
            if pauseState == False:
                os.system('avconv -re -i "/media/pi/PIWALL/%s" -vcodec copy -f avi -an udp://239.0.1.23:1234' % values)
                    
    def load(self):
        #scan and load media
        global listvideos
        self.listbox1.delete(0,'end')
        for video in glob.glob('/media/pi/PIWALL/*.mp4'):
            video.split("/")
            a,b,c,d,videofiles = video.split("/")
            self.listbox1.insert('end', str(videofiles))
            self.listbox1.itemconfig('end', {'fg':'white'})
            listvideos = True
            print videofiles
    
    def clear(self):
        global listvideos
        self.listbox1.delete(0,'end')
        values=None
        listvideos = False
        print "listbox clear"
        
    def select_item(self, event):
        global values
        widget = event.widget
        selection=widget.curselection()
        if listvideos == True:
            values = widget.get(selection[0])
            print "selection:", selection, ": '%s'" % values
        else:
            self.tk.option_add('*Dialog.msg.font', 'Calibri 10')
            self.tk.resizable(0,0)
            self.tk.overrideredirect(1)
            tkMessageBox.showwarning("Empty Library","Insert PIWALL USB and press Load Button")
            print "list empty"
    def counter_button(self):
        global btnCounter
        if btnCounter == 0:
            btnCounter += 1
            print "on"
        elif btnCounter >= 0:
            btnCounter = 0
            print "off"
            
                            
    def create_widgets(self):
        #create Play button
        self.buttonPlay = Button(frame, command=self.play_movie, bd=0,highlightthickness = 0,bg="black", activebackground="yellow")
        self.buttonPlay.grid(row=0, column=2)
        imagePlay = ImageTk.PhotoImage(file="asset/p.png")
        self.buttonPlay.config(image = imagePlay)
        self.buttonPlay.image = imagePlay

        #create Stop button
        self.buttonStop = Button(frame, command = self.stop_movie, bd=0,highlightthickness = 0, bg="black", activebackground="yellow")
        self.buttonStop.grid(row=0, column=3)
        imageStop = ImageTk.PhotoImage(file="asset/s.png")
        self.buttonStop.config(image = imageStop)
        self.buttonStop.image = imageStop
        
        #create Blank button
        #self.buttonBlank = Button(frame, command = self.blank_movie, bd=0, bg="white", activebackground="yellow")
        #self.buttonBlank.grid(row=0, column=2)
        #imageBlank = ImageTk.PhotoImage(file="asset/b.png")
        #self.buttonBlank.config(image = imageBlank)
        #self.buttonBlank.image = imageBlank
        
        #create eject EXT Drive
        self.buttonEject = Button(frame, command = self.eject, bd=0,highlightthickness = 0, bg="black", activebackground="yellow")
        self.buttonEject.grid(row = 0, column = 0)
        imageEject = ImageTk.PhotoImage(file="asset/b.png")
        self.buttonEject.config(image = imageEject)
        self.buttonEject.image = imageEject            
           
        #create Next option
        self.buttonNext = Button(frame, command = self.counter_button, bd=0,highlightthickness = 0, bg="blacK", activebackground="yellow")
        self.buttonNext.grid(row = 0, column = 1)
        imageNext = ImageTk.PhotoImage(file="asset/b.png")
        self.buttonNext.config(image = imageNext)
        self.buttonNext.image = imageNext
            
        #create Shutdown Clusters
        self.buttonShut = Button(frame,command = self.shut_cluster, bd=0,highlightthickness = 0, bg="black", activebackground="yellow")
        self.buttonShut.grid(row = 0, column = 4)
        imageShut = ImageTk.PhotoImage(file="asset/sh.png")
        self.buttonShut.config(image = imageShut)
        self.buttonShut.image = imageShut
        
        #Create Button Load
        self.buttonLoad = Button(frame2, text ="Load Videos", command = self.load, bd=0,highlightthickness = 0, bg="black", activebackground ="yellow")
        self.buttonLoad.grid(row=0, column = 4, sticky=W+N)
        imageLoad = ImageTk.PhotoImage(file="asset/l.png")
        self.buttonLoad.config(image = imageLoad)
        self.buttonLoad.image = imageLoad
        
         #Create Button clear
        self.buttonClear = Button(frame2, text ="Clear Videos", command = self.clear, bd=0,highlightthickness = 0, bg="black", activebackground ="yellow")
        self.buttonClear.grid(row=1, column = 4, sticky=W+N)
        imageClear = ImageTk.PhotoImage(file="asset/r.png")
        self.buttonClear.config(image = imageClear)
        self.buttonClear.image = imageClear
        
        #create listbox with scrollbar
        self.scrollbar_V = Scrollbar(frame2, width=10, bg="black", troughcolor="black", relief="flat", highlightthickness=0, activebackground="yellow")
        #self.scrollbar_H = Scrollbar(frame2, orient=HORIZONTAL, width=10, bg="white", troughcolor="white")
        self.scrollbar_V.grid(row=0, column=0, rowspan=2, sticky=N+S+E)
        #self.scrollbar_H.grid(row=1, column=0, columnspan=2, sticky=N+E+S+W)
        
        self.listbox1 = Listbox(frame2, font=('calibri', 12), bg="black",highlightthickness = 0, relief="flat", width=38, height=12, yscrollcommand=self.scrollbar_V.set)#xscrollcommand=self.scrollbar_H.set
        self.listbox1.bind('<<ListboxSelect>>', self.select_item)
        self.listbox1.grid(row=0, column=1, columnspan=2, rowspan=2, sticky=W+E+N)
        
        self.scrollbar_V.config(command=self.listbox1.yview)
        #self.scrollbar_H.config(command=self.listbox1.xview)
    
    def toggle_fullscreen(self, event=True):
        self.state = not self.state  # Just toggling the boolean
        self.tk.attributes("-fullscreen", self.state)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.tk.attributes("-fullscreen", False)
        return "break"

    def play_movie(self):
        imagePlay = None
        global t1
        global playState
        global pauseState

        if playState == False:
            playState = True
            pauseState = False
            t1= threading.Thread(target=self.play, args=())
            imagePlay = ImageTk.PhotoImage(file="asset/p2.png")

            t1.start()
        elif playState == True:
            if pauseState == False:
                pauseState = True
                pid = get_pid("avconv")
		for item in pid:
			os.kill(int(item), signal.SIGSTOP)
			print(int(item))
                imagePlay = ImageTk.PhotoImage(file="asset/p.png")
                
            else:
                pid = get_pid("avconv")
                for item in pid:
                        os.kill(int(item), signal.SIGCONT)
			print(int(item))
                pauseState = False
                imagePlay = ImageTk.PhotoImage(file="asset/p2.png")

        self.buttonPlay.config(image = imagePlay)
        self.buttonPlay.image = imagePlay
        
    def stop_movie(self):
        global playState
        imagePlay = ImageTk.PhotoImage(file="asset/p.png")
        self.buttonPlay.config(image = imagePlay)
        self.buttonPlay.image = imagePlay
        playState = False
        os.system('sudo killall avconv')
        
    def blank_movie(self):
        self.tk.option_add('*Dialog.msg.font', 'Calibri 10')
        self.tk.resizable(0,0)
        self.tk.overrideredirect(1)
        tkMessageBox.showwarning("","Beta Ver.03")
        print("Digital Nativ")
    
    def eject(self):
        os.system('umount /media/irvan/PIWALL')
        self.listbox1.delete(0,'end')
        values=None
        self.tk.option_add('*Dialog.msg.font', 'Calibri 10')
        self.tk.resizable(0,0)
        self.tk.overrideredirect(1)
        tkMessageBox.showwarning("","Drive Unmount")
    
    def next_movie(self):
        os.system('sh shutdownall.sh')
        
    def shut_cluster(self):
        os.system('sh /home/pi/shutdownall.sh')
        #self.load()

if __name__ == '__main__':
    w = Fullscreen_Window()    
    w.tk.mainloop()
