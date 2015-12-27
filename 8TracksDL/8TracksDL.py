#!/usr/bin/python

import Tkinter
import requests
import tkFileDialog
import json
import subprocess
from os.path import expanduser

def get_Play_Token():
    try:
	f = open(expanduser("~/Library/Cookies/Cookies.binarycookies"))
    except:
	print "Failed to open cookie fail and retrieve play_token"
	return 0

    raw = f.read()

    try:
	text = raw.split("play_token")
	play_token = ""
	for i in range(15):
	    if text[1][i].isdigit():
		play_token += text[1][i]
    except:
	print "Failed to find play_token in cookie file"
	return 0

    return int(play_token)

    
def get_MixID(mixURL):
    try:
	r = requests.get(mixURL)
    except:
	print "HTTP request for mix url failed"
	return 0

    try:
	raw = (r.text)
	text = raw.split("mix_id")
	i = 2
	mixID  = ""
	while text[1][i].isdigit():
	    mixID += text[1][i]
	    i += 1

    except:
	print "Could not parse to find mix ID"
	return 0

    return int(mixID)


def download():
    mixURL = urlEntry.get()
    play_token = get_Play_Token()
    mixID = get_MixID(mixURL)

    path = "http://8tracks.com/sets/" + str(play_token) + "/play?"
    path += "mix_id=" + str(mixID) + "&format=jsonh"

    try:
	r = requests.get(path)
    except:
	print "Could not access play info for current song"
	return 0

    info = json.loads(r.text)
    dlURL = info['set']['track']['track_file_stream_url']
    name = info['set']['track']['name']
    artist = info['set']['track']['performer']

    print ("Downloading " + name + " by " + artist + "...") 
    savename =str(dlPath.get()) + "/"  + name + " - " + artist + ".mp4"
    print savename
    r = requests.get(dlURL)
    f = open(savename, "w")
    f.write(r.content)
    f.close
    print "Finished Download"


def change_Path():
    new_path = str(tkFileDialog.askdirectory(mustexist="true"))
    current_path = dlPath.get()
    if len(new_path) > 1:
	dlPath.delete(0, len(current_path)-1)
	dlPath.insert(0, new_path)

window = Tkinter.Tk()
window.wm_title("Download 8tracks songs")
frame = Tkinter.Frame(window)
frame.pack()

dlPathFrame = Tkinter.Frame(window)
dlPathFrame.pack(side = Tkinter.BOTTOM)

urlLabel = Tkinter.Label(frame, text="Playlist URL")
urlLabel.pack(side = Tkinter.LEFT)

urlEntry = Tkinter.Entry(frame, width=40)
urlEntry.pack(side = Tkinter.LEFT)
urlCmd = """osascript -e 'tell application \"Safari\" to get the URL of every tab of every window'"""
openTabs = subprocess.check_output(urlCmd, shell=True)
openTabsList = openTabs.split(",")
for url in openTabsList:
    if "8tracks" in url:
	defaultUrl = url
if "8tracks" in defaultUrl:
    defaultUrl = defaultUrl.strip(" ")
    urlEntry.insert(0, defaultUrl)
else:
    print ("Could not get automatically get playlist URL")

dlButton=Tkinter.Button(frame,text="Download Song",command=download)
dlButton.pack(side = Tkinter.RIGHT)

dlPathLabel = Tkinter.Label(dlPathFrame, text="Download Path")
dlPathLabel.pack(side=Tkinter.LEFT)

dlPathButton=Tkinter.Button(dlPathFrame,text="Change Path",command=change_Path)
dlPathButton.pack(side=Tkinter.RIGHT)

dlPath = Tkinter.Entry(dlPathFrame, width=35)
defaultPath = expanduser("~/Downloads")
dlPath.insert(0, defaultPath)
dlPath.pack(side=Tkinter.LEFT)

window.mainloop()
