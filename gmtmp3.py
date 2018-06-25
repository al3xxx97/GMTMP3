#!/usr/bin/env python3
from __future__ import unicode_literals
from time import sleep
from subprocess import *
import sys
import youtube_dl
import urllib.request
import urllib.parse
import re
import os
import glob
import RPi.GPIO as GPIO
import lcd
import time
import ftplib

#FTP LOGIN DATA
HOST = "192.168.43.167"
PORT = 2121

# Button definiton
downloadbutton = 21
nextbutton = 20

GPIO.setmode(GPIO.BCM)
GPIO.setup(downloadbutton, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(    nextbutton, GPIO.IN, pull_up_down = GPIO.PUD_UP)


def runCMD(cmd):
    com = Popen(cmd, shell=True, stdout=PIPE)
    shellOutput = com.communicate()
    return shellOutput[0]

def next(nextbutton):
     runCMD("mpc next")

def download(downloadbutton):
    print('Download started...')
    lcd.printString("Downloading...", lcd.line1)
    time.sleep(5)
    file = open("song.txt","r")
    song = file.readline()
    file.close()
    query_string = urllib.parse.urlencode({"search_query" : song})
    html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
    id = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
    xdel = open("song.txt","w").close()
    xdel2 = open("songname.txt","w")
    xdel2.write("''")
    xdel2.close()
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192'
    }]}

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([id[0]])


    for name in glob.glob('/home/pi/music' + id[0] +'*'):
        name = name.replace('/home/pi/music/', "")
        songname = open("songname.txt","w")
        songname.write(name)
        songname.close()
        print(name)
        ftp=ftplib.FTP()
        myftp = ftp.connect(HOST,PORT)
        ftp.login()
        filename = open("songname.txt","r")
        name = filename.readline()
        filename.close()
        fh = open(name, 'rb')
        ftp.storbinary('STOR %s.mp3' % name ,fh)
        print("uploaded")


if __name__ == "__main__":
    GPIO.add_event_detect(nextbutton,GPIO.FALLING, callback = next , bouncetime = 250)
    GPIO.add_event_detect(downloadbutton,GPIO.FALLING, callback = download, bouncetime = 250)

    lcd.init()
    while(1<2):
        cmdIP = "mpc play | head -n 1"
        strIP = runCMD(cmdIP)
        song = open("song.txt","w")
        song.write(str(strIP))
        song.close()
        lcd.printString(str(strIP),lcd.line1)
        lcd.printString(str(strIP),lcd.line2)
        lcd.sleep(5)
        
