version = '0.1.0'

import os
import tkinter as tk
import pygetwindow as gw
from PIL import Image, ImageTk
import pathlib
import configparser
from ahk import AHK
import functions

config = configparser.ConfigParser()
config.read('config.ini')

display = config.getint('window', 'display')
show_x = config.getint('window', 'x')
show_y = config.getint('window', 'y')
alwaysontop = config.get('window', 'alwaysontop')
borderless = config.get('window', 'borderless')
untranslucentpercentage = config.getint('window', 'untranslucentpercentage')
alwaysvisibility = config.get('window', 'alwaysvisibility')
refreshinterval = config.getint('window', 'refreshinterval')
hotkey = config.get('window', 'hotkey')
overlay_path = config.get('ninb', 'overlay')
ninbsize = config.getint('ninb', 'size')  # 1=small, 2=medium, 3=large
header = config.get('ninb', 'header')
row = config.getint('ninb', 'row')
detailsheader = config.get('ninb', 'detailsheader')
detailsrow = config.getint('ninb', 'detailsrow')
boaticonpos = config.getint('ninb', 'boaticonpos')  # 0=not used, 1=top left, 2=top right
boaticon_width = config.getint('ninb', 'boaticon_width')
boaticon_height = config.getint('ninb', 'boaticon_height')
notify_newversion = config.get('other', 'notify_newversion')

root = tk.Tk()
root.resizable(False, False)
root.attributes('-topmost',alwaysontop)
root.overrideredirect(borderless)
root.attributes('-alpha',untranslucentpercentage/100)
root.geometry(f'0x0+{int(functions.get_display_values(functions.choose_display(display), 0))+show_x}+{int(functions.get_display_values(functions.choose_display(display), 1))+show_y}')
root.title(f'Ninb Viewer v{version}')

img_data = pathlib.Path(overlay_path)
old_data = 0
togglebyte = 1500
winstate = 1
mctitle = 'Minecraft'
hotkey = hotkey

ahk = AHK()

if notify_newversion == 'True':
  functions.version_check(version)

def refresh():
  if datacheck():
    main()
  root.after(refreshinterval , refresh)

def main():
  global img
  img = Image.open(overlay_path)

  if ninbsize == 1:
    window_width = img.width
    if 1 <= boaticonpos:
      boatimg = img.crop((img.width-114,4,img.width-94,24))
      boatimg = boatimg.resize((boaticon_width,boaticon_height))
    if 0 < detailsrow < 4:
      if detailsheader:
        detailimg = img.crop((0,img.height-65,img.width,img.height-(3-detailsrow)*16))
      else:
        detailimg = img.crop((0,img.height-48,img.width,img.height-(3-detailsrow)*16))
    if header:
      crop_y = 25
      crop_height = (row * 20) + 23 + detailimg.height
    else:
      crop_y = 48
      crop_height = (row * 20) + detailimg.height
  elif ninbsize == 2:
    window_width = img.width
    if 1 <= boaticonpos:
      boatimg = img.crop((img.width-114,4,img.width-94,24))
      boatimg = boatimg.resize((boaticon_width,boaticon_height))
    if 0 < detailsrow < 4:
      if detailsheader:
        detailimg = img.crop((0,img.height-71,img.width,img.height-(3-detailsrow)*18))
      else:
        detailimg = img.crop((0,img.height-54,img.width,img.height-(3-detailsrow)*18))
    if header:
      crop_y = 26
      crop_height = row * 23 + 25 + detailimg.height
    else:
      crop_y = 51
      crop_height = row * 23 + detailimg.height
  elif ninbsize == 3:
    window_width = img.width
    if 1 <= boaticonpos:
      boatimg = img.crop((img.width-114,4,img.width-94,24))
      boatimg = boatimg.resize((boaticon_width,boaticon_height))
    if 0 < detailsrow < 4:
      if detailsheader:
        detailimg = img.crop((0,img.height-106,img.width,img.height-(3-detailsrow)*28))
      else:
        detailimg = img.crop((0,img.height-84,img.width,img.height-(3-detailsrow)*28))
    if header:
      crop_y = 27
      crop_height = row * 33 + 34 + detailimg.height
    else:
      crop_y = 61
      crop_height = row * 33 + detailimg.height
                                                               
  img = img.crop((0,crop_y-2,window_width,crop_y+crop_height))
  img = img.resize((window_width,crop_height))
  if 0 < detailsrow < 4:
    img.paste(detailimg, (0, crop_height-detailimg.height))
  if boaticonpos == 1:
    img.paste(boatimg, (0, 0))
  if boaticonpos == 2:
    img.paste(boatimg, (img.width-boaticon_width, 0))
  if 0 < detailsrow < 4:
    canvas = tk.Canvas(root, width=window_width, height=crop_height+detailimg.height)
  else:
    canvas = tk.Canvas(root, width=window_width, height=crop_height)
  canvas.place(x=-2, y=-2)
  img = ImageTk.PhotoImage(img)
  
  canvas.create_image(0, 0, image=img, anchor=tk.NW,tag='dummy')
  canvas.itemconfig('dummy', image=img, anchor=tk.NW)

  root.geometry(f'{window_width-2}x{crop_height-2}')

def datacheck():
  global old_data, winstate
  data = img_data.stat().st_mtime
  if old_data < data:
    if alwaysvisibility and togglebyte <= os.path.getsize(overlay_path):
      old_data = data
      winstate = 1
      root.deiconify()
      return True
    elif alwaysvisibility and togglebyte > os.path.getsize(overlay_path):
      root.withdraw()
      return False
    else:
      old_data = data
      return True
  return False

def wintoggle():
  global winstate
  mcwindow = ahk.find_window(title=mctitle)
  if mcwindow.active and togglebyte <= os.path.getsize(overlay_path):
    if winstate:
      winstate = 0
      root.withdraw()
    else:
      winstate = 1
      root.deiconify()

if __name__ == '__main__':
  ahk.add_hotkey(hotkey, callback=wintoggle)
  ahk.start_hotkeys()
  refresh()
  root.mainloop()