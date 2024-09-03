import os
import shutil
import tkinter as tk
import pygetwindow as gw
from PIL import Image, ImageTk
import mss
import mss.tools
import time
from pathlib import Path

# --- Options ---
overlay_path = R'C:\Users\PC_User\AppData\Local\Temp\nb-overlay.png'  # path of ninb OBS overlay
show_x = 0
show_y = 0
ninbsize = 0  # 0=small, 1=medium, 2=large
header = True
row = 1
boaticonpos = 1  # -1=not used, 0=top left, 1=top right
boaticon_width = 20
boaticon_height = 20
detailsheader = True
detailsrow = 1
alwaysontop = True
borderless = True
refreshinterval = 2000

# Do Not Edit
version = 'DEV'

root = tk.Tk()
root.resizable(False, False)
root.attributes('-topmost',alwaysontop)
root.overrideredirect(borderless)

def refresh():
  files_file = take_screenshot('Ninjabrain Bot','./data/screenshot')
  if 1 == len(files_file):
    startup()

  global img
  img = Image.open(f'./data/screenshot/{files_file[1]}')
  os.remove(f'./data/screenshot/{files_file[0]}')

  if ninbsize == 0:
    window_width = img.width
    if 0 <= boaticonpos:
      boatimg = img.crop((img.width-114,5,img.width-94,23))
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
  elif ninbsize == 1:
    window_width = img.width
    if 0 <= boaticonpos:
      boatimg = img.crop((img.width-114,5,img.width-94,23))
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
  elif ninbsize == 2:
    window_width = img.width
    if 0 <= boaticonpos:
      boatimg = img.crop((img.width-114,5,img.width-94,23))
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

  root.geometry(f'{window_width-2}x{crop_height-2}+{show_x}+{show_y}')
  root.title(f'Ninb Viewer v{version}')
                                                                 
  img = img.crop((0,crop_y-2,window_width,crop_y+crop_height))
  img = img.resize((window_width,crop_height))
  if 0 < detailsrow < 4:
    img.paste(detailimg, (0, crop_height-detailimg.height))
  if boaticonpos == 0:
    img.paste(boatimg, (0, 0))
  if boaticonpos == 1:
    img.paste(boatimg, (img.width-boaticon_width, 0))
  if 0 < detailsrow < 4:
    canvas = tk.Canvas(root, width=window_width, height=crop_height+detailimg.height)
  else:
    canvas = tk.Canvas(root, width=window_width, height=crop_height)
  canvas.place(x=-2, y=-2)
  img = ImageTk.PhotoImage(img)
  
  item = canvas.create_image(0, 0, image=img, anchor=tk.NW,tag='dummy')
  canvas.itemconfig('dummy', image=img, anchor=tk.NW)
  root.after(refreshinterval , refresh)

# https://github.com/yo16/take_screenshot_continuous
def take_screenshot(window_title: str, save_to_dir: str):
  windows = gw.getWindowsWithTitle(window_title)
  if not windows:
    print("No matching window found.")
    return 
    
  window = windows[0]
  left, top, width, height = window.left, window.top, window.width, window.height
  take_screenshot_by_mss(left, top, width, height, save_to_dir)

  dir_path = './data/screenshot'
  return [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]

def take_screenshot_by_mss(x: int, y: int, width: int, height: int, save_to: str):
  print(f'x:{x}, y:{y}, w:{width}, h:{height}')
    
  dir_path = Path(save_to)
  dir_path.mkdir(parents=True, exist_ok=True)

  with mss.mss() as sct:
    monitor = {'top': y, 'left': x, 'width': width, 'height': height}
    screenshot = sct.grab(monitor)
      
    current_time = time.localtime()
    time_str: str = time.strftime('%Y%m%d_%H%M%S', current_time)
    file_path: Path = dir_path / f'{time_str}.png'
      
    mss.tools.to_png(screenshot.rgb, screenshot.size, output=str(file_path))
    print(f"Screenshot taken and saved as '{file_path}'")

def startup():
  target_dir = './data/screenshot'
  shutil.rmtree(target_dir)
  os.mkdir(target_dir)
  dummy = take_screenshot('Ninjabrain Bot','./data/screenshot')

if __name__ == '__main__':
  root.after(0,refresh)
  root.mainloop()