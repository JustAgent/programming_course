import os
import re
from tkinter import *
from tkinter.ttk import Combobox

path = "./"
main = []
sub = []
for root, dirs, files in os.walk(path):
    for file in files:
        if (file.endswith(".pdf")):
            temp = file
            temp = re.sub(r"20\d\d-\d\d-\d\d - ", "", temp)
            temp = re.sub(r".pdf", "", temp)
            main.append(file)
            sub.append(temp)
# print(main)
# print(sub)

output_file = ""


def clicked():
    file_name = combo_ticker.get()
    print("SUB: " , file_name)
    i = None
    i = sub.index(file_name)
    a = "./" + main[i]
    print("MAIN: " , a)
    os.system(a)


Iwindow = Tk()
Iwindow.title("Shares analysis")
lbl = Label(Iwindow, text="Choose token")
Iwindow.geometry('400x400')
combo_ticker = Combobox(Iwindow)
combo_ticker['values'] = tuple(sub)
combo_ticker.current(0)
combo_ticker.grid(column=2, row=2)
btn = Button(Iwindow, text="Don't touch!", command=clicked)
btn.grid(column=2, row=5)

Iwindow.mainloop()