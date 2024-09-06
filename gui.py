version = '0.1.0'

import tkinter as tk
import tkinter.filedialog
from tkinter import ttk
from ttkthemes import *
from tkinter import messagebox
import configparser
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

# colors
bg1 = '#55585a'
bg2 = '#424242'
fg = '#ffffff'
abg = '#446e9e'
tr = '#3c3f41'
hl = '#3c3f41'
sl = '#3c3f41'
sty = '#55585a'

root = ThemedTk(theme='black')
style = ttk.Style()
style.configure('TLabel', background=bg1, foreground=fg)
style.configure('TCombobox', fieldbackground= f'{sty}', background= f'{sty}', foreground=fg)
root.option_add("*TCombobox*Listbox*Background", f'{sty}')
root.option_add('*TCombobox*Listbox*Foreground', f'{fg}')
root.option_add('*TCombobox*Listbox*selectBackground', f'{sty}')
root.option_add('*TCombobox*Listbox*selectForeground', f'{fg}')

root.resizable(False, False)
#root.attributes('-topmost', alwaysontop)
root.geometry(f'382x275')
root.title(f'Ninview Settings v{version}')
root.iconbitmap(default='blaze_powder.ico')

note = ttk.Notebook(root, width=382, height=275)
tab = []
for l in range(3):
  tab.append(ttk.Frame(root))

if notify_newversion == 'True':
  functions.version_check(version)

# def
def openfile():
  file_name = tkinter.filedialog.askopenfilename(filetypes=[('PNG', '.png')], initialdir='C:\\')
  overlay_path_entry.configure(state='normal')
  print(file_name)
  if file_name:
    overlay_path_entry.delete(0, tk.END)
    overlay_path_entry.insert(tk.END,file_name)
  overlay_path_entry.configure(state='readonly')
  
def save():
  try:
    dummy = int(x_entry.get())
    dummy = int(y_entry.get())

    config['window']['display'] = str(choose_monitor_scale.get())
    config['window']['x'] = str(x_entry.get())
    config['window']['y'] = str(y_entry.get())
    config['window']['alwaysontop'] = str(alwaysontop_var.get())
    config['window']['borderless'] = str(borderless_var.get())
    config['window']['untranslucentpercentage'] = str(untranslucentpercentage_scale.get())
    config['window']['alwaysvisibility'] = str(alwaysvisibility_var.get())
    config['window']['refreshinterval'] = str(int(refreshinterval_scale.get()*1000))
    config['window']['hotkey'] = str(hotkey_entry.get())
    config['ninb']['overlay'] = str(overlay_path_entry.get().replace('/', '\\'))
    config['ninb']['size'] = str(choose_size_scale.get())
    config['ninb']['header'] = str(header_var.get())
    config['ninb']['row'] = str(row_scale.get())
    config['ninb']['detailsheader'] = str(detailsheader_var.get())
    config['ninb']['detailsrow'] = str(detailsrow_scale.get())
    if boat_combobox.get() == '左上':
      config['ninb']['boaticonpos'] = str(1)
    elif boat_combobox.get() == '右上':
      config['ninb']['boaticonpos'] = str(2)
    else:
      config['ninb']['boaticonpos'] = str(0)
    config['ninb']['boaticon_width'] = str(boatwidth_scale.get())
    config['ninb']['boaticon_height'] = str(boatheight_scale.get())
    config['other']['notify_newversion'] = str(notify_newversion_var.get())

    with open('config.ini', 'w') as f:
      config.write(f)
    
    for l in range(3):
      save_label[l].place(x=251, y=214)
    root.after(3000, savetext_hide)
  except ValueError:
    messagebox.showerror('エラー', 'X座標、またはY座標に数値以外が入力されています', detail='保存は実行されていません')

def savetext_hide():
  for l in range(3):
    save_label[l].place_forget()

# tab 1
choose_monitor_scale = tk.Scale(
  tab[0], from_=1, to=functions.get_display(), resolution=1, orient='horizontal',
  background=bg1, foreground=fg, activebackground=abg, troughcolor=tr, highlightcolor=hl, highlightthickness=0,
  label='モニター', sliderrelief='flat'
  )
choose_monitor_scale.place(x=10, y=10)
choose_monitor_scale.set(display)

x_label = tk.Label(tab[0], text='X:', width=1, background=bg2, foreground=fg)
x_label.place(x=122, y=25)

x_entry = tk.Entry(tab[0], width=6, background=bg1, foreground=fg, borderwidth=0)
x_entry.place(x=139, y=27)
x_entry.insert(0, show_x)

y_label = tk.Label(tab[0], text='Y:', width=1, background=bg2, foreground=fg)
y_label.place(x=187, y=25)

y_entry = tk.Entry(tab[0], width=6, background=bg1, foreground=fg, borderwidth=0)
y_entry.place(x=204, y=27)
y_entry.insert(0, show_y)

untranslucentpercentage_scale = tk.Scale(
  tab[0], from_=0, to=100, resolution=5, orient='horizontal',
  background=bg1, foreground=fg, activebackground=abg, troughcolor=tr, highlightcolor=hl, highlightthickness=0,
  label='不透明度', sliderrelief='flat'
  )
untranslucentpercentage_scale.place(x=10, y=75)
untranslucentpercentage_scale.set(untranslucentpercentage)

refreshinterval_scale = tk.Scale(
  tab[0], from_=0, to=10, resolution=0.05, orient='horizontal',
  length=244, background=bg1, foreground=fg, activebackground=abg, troughcolor=tr, highlightcolor=hl, highlightthickness=0,
  label='更新間隔（秒）', sliderrelief='flat'
  )
refreshinterval_scale.place(x=122, y=75)
refreshinterval_scale.set(refreshinterval/1000)

alwaysontop_var = tk.BooleanVar() ; alwaysontop_var.set(alwaysontop)
alwaysontop_checkbox = tk.Checkbutton(tab[0], text='常に最前列に表示', background=bg2, activebackground=bg2, foreground=fg, activeforeground=fg, selectcolor=sl, variable=alwaysontop_var)
alwaysontop_checkbox.place(x=10, y=140)

borderless_var = tk.BooleanVar() ; borderless_var.set(borderless)
borderless_checkbox = tk.Checkbutton(tab[0], text='ボーダーレス', background=bg2, activebackground=bg2, foreground=fg, activeforeground=fg, selectcolor=sl, variable=borderless_var)
borderless_checkbox.place(x=138, y=140)

alwaysvisibility_var = tk.BooleanVar() ; alwaysvisibility_var.set(alwaysvisibility)
alwaysvisibility_checkbox = tk.Checkbutton(tab[0], text='常に表示', background=bg2, activebackground=bg2, foreground=fg, activeforeground=fg, selectcolor=sl, variable=alwaysvisibility_var)
alwaysvisibility_checkbox.place(x=229, y=140)

hotkey_label = tk.Label(tab[0], text='ホットキー:', width=6, background=bg2, foreground=fg)
hotkey_label.place(x=10, y=175)

hotkey_entry = tk.Entry(tab[0], width=26, background=bg1, foreground=fg, borderwidth=0)
hotkey_entry.place(x=62, y=177)
hotkey_entry.insert(0, hotkey)

# tab 2
overlay_path_entry = tk.Entry(tab[1], width=51, readonlybackground=bg1, foreground=fg, relief='flat', state='normal')
overlay_path_entry.place(x=10, y=14)
overlay_path_entry.insert(0, overlay_path)
overlay_path_entry.configure(state='readonly')

button = tk.Button(tab[1], width=4, text='参照', background=bg1, foreground=fg, activebackground=abg, relief='flat', command=openfile)
button.place(x=330, y=11)

choose_size_scale = tk.Scale(
  tab[1], from_=1, to=3, resolution=1, orient='horizontal',
  background=bg1, foreground=fg, activebackground=abg, troughcolor=tr, highlightcolor=hl, highlightthickness=0,
  label='Ninb サイズ', sliderrelief='flat'
  )
choose_size_scale.place(x=10, y=47)
choose_size_scale.set(ninbsize)

row_scale = tk.Scale(
  tab[1], from_=1, to=5, resolution=1, orient='horizontal',
  background=bg1, foreground=fg, activebackground=abg, troughcolor=tr, highlightcolor=hl, highlightthickness=0,
  label='表示する行数', sliderrelief='flat'
  )
row_scale.place(x=152, y=47)
row_scale.set(row)

detailsrow_scale = tk.Scale(
  tab[1], from_=1, to=3, resolution=1, orient='horizontal',
  background=bg1, foreground=fg, activebackground=abg, troughcolor=tr, highlightcolor=hl, highlightthickness=0,
  label='表示する詳細の行数', sliderrelief='flat'
  )
detailsrow_scale.place(x=264, y=47)
detailsrow_scale.set(detailsrow)

header_var = tk.BooleanVar() ; header_var.set(header)
header_checkbox = tk.Checkbutton(tab[1], text='ヘッダーを表示', background=bg2, activebackground=bg2, foreground=fg, activeforeground=fg, selectcolor=sl, variable=header_var)
header_checkbox.place(x=10, y=112)

detailsheader_var = tk.BooleanVar() ; detailsheader_var.set(detailsheader)
detailsheader_checkbox = tk.Checkbutton(tab[1], text='詳細ヘッダーを表示', background=bg2, activebackground=bg2, foreground=fg, activeforeground=fg, selectcolor=sl, variable=detailsheader_var)
detailsheader_checkbox.place(x=116, y=112)

boat_label = tk.Label(tab[1], text='ボートアイコン:', width=9, background=bg2, foreground=fg)
boat_label.place(x=10, y=162)

boat_option =['非表示', '左上', '右上']
boat_combobox = ttk.Combobox(tab[1], width=6, values=boat_option, textvariable=tk.StringVar(), state='readonly')
boat_combobox.place(x=84, y=163)
boat_combobox.set(boat_option[boaticonpos])

boatwidth_scale = tk.Scale(
  tab[1], from_=20, to=40, resolution=1, orient='horizontal',
  background=bg1, foreground=fg, activebackground=abg, troughcolor=tr, highlightcolor=hl, highlightthickness=0,
  label='ボートアイコンの幅', sliderrelief='flat'
  )
boatwidth_scale.place(x=152, y=147)
boatwidth_scale.set(boaticon_width)

boatheight_scale = tk.Scale(
  tab[1], from_=20, to=40, resolution=1, orient='horizontal',
  background=bg1, foreground=fg, activebackground=abg, troughcolor=tr, highlightcolor=hl, highlightthickness=0,
  label='ボートアイコンの高さ', sliderrelief='flat'
  )
boatheight_scale.place(x=264, y=147)
boatheight_scale.set(boaticon_height)

# tab 3
notify_newversion_var = tk.BooleanVar() ; notify_newversion_var.set(notify_newversion)
notify_newversion_checkbox = tk.Checkbutton(tab[2], text='新たなリリースがある場合に通知する', background=bg2, activebackground=bg2, foreground=fg, activeforeground=fg, selectcolor=sl, variable=notify_newversion_var)
notify_newversion_checkbox.place(x=10, y=10)

# tab 1 ~ 3
save_label = []
save_button = []
for l in range(3):
  save_label.append(tk.Label(tab[l], text='保存しました！', width=9, background=bg2, foreground=fg))
  save_label[l].place(x=251, y=214)
  save_label[l].place_forget()

  save_button.append(tk.Button(tab[l], text='保存', width=4, background=bg1, foreground=fg, activebackground=abg, relief='flat', command=save))
  save_button[l].place(x=330, y=212)

# add tab
note.add(tab[0], text='ウインドウ')
note.add(tab[1], text='Ninb')
note.add(tab[2], text='その他')
note.pack()

if __name__ == '__main__':
  root.mainloop()