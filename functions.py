import re
from screeninfo import get_monitors
import requests
from tkinter import messagebox
import webbrowser

def get_display():
  n = 0
  for m in get_monitors():
    n += 1
  return n

def choose_display(display):
  list = []
  for m in get_monitors():
    list.append(str(m))
  return list[display-1]

def get_display_values(display, n):
  list = re.findall('[-0-9]+', display)
  return list[n]

def version_check(version):
  url = 'https://raw.githubusercontent.com/mebuki117/ninb-viewer/main/meta'
  data = requests.get(url).content
  if str(version) < str(data).replace('b', '').replace("'", ''):
    m = messagebox.askquestion('Ninb Viewer', '新しいリリースがあります', detail='ダウンロードページを開きますか？')
    if m == 'yes':
      webbrowser.open('https://github.com/mebuki117/ninb-viewer/releases')