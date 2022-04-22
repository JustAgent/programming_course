import yfinance as yf
import matplotlib.pyplot as plt
import random
import math
from random import randint
import numpy as np


def destroyer(array, count):
    for i in range(count):
        while True:
            x = random.randint(0, len(array) - 1)
            if array[x] != None: break
        array[x] = None
    print("destroyer works")
    return array


# approx
def approximation(a):
    for x in range(len(a)):
        if a[x] == None:
            i, j = 1, 1
            i2, j2 = 1, 1
            flag1 = False
            flag2 = False
            counter = 0
            counter2 = 0

            while True and not flag1:
                if x + i < len(a):
                    if a[x + i] is not None:
                        y2 = a[x + i]
                        x2 = x + 1 + i
                        break
                    i += 1

                else:
                    if counter < 2:
                        while True:
                            if x - j >= 0:
                                if a[x - j] is not None:
                                    counter += 1
                                    if counter == 2:
                                        y2 = a[x - j]
                                        x2 = x + 1 - j
                                        flag1 = True
                                        break
                                j += 1

            while True and not flag2:
                if x - i2 >= 0:
                    if a[x - i2] is not None:
                        y1 = a[x - i2]
                        x1 = x + 1 - i2
                        break
                    i2 += 1

                else:
                    if counter2 < 2:
                        while True:
                            if x + j2 < len(a):
                                if a[x + j2] is not None:
                                    counter2 += 1
                                    if counter2 == 2:
                                        y1 = a[x + j2]
                                        x1 = x + 1 + j2
                                        flag2 = True
                                        break
                                j2 += 1

            k = (y2 - y1) / (x2 - x1)
            b = y1 - (k * x1)
            a[x] = k * (x + 1) + b
    print("approx works")
    return a


# винзолирование
def vinz(array):
    for i in range(len(array)): recover(i, array)
    print("vinz works")
    return array


def correlation(array, array2):
    list_y = array
    list_x = []
    sum_x = 0
    sum_y = 0
    list_x = array2

    # for i in range(1, len(array) + 1):
    #     list_x.append(i)
    copied_array = array.copy()
    zero_counter = 0
    for i in range(len(list_x)):
        if list_y[i] != 0:
            sum_x += list_x[i]
            sum_y += list_y[i]
        else:
            zero_counter += 1

    average_x = sum_x / (len(list_x) - zero_counter)
    average_y = sum_y / (len(list_y) - zero_counter)
    disp_sum_up = 0
    disp_sum_down_x = 0
    disp_sum_down_y = 0

    for i in range(len(list_x)):
        if list_y[i] != 0:
            disp_sum_up += (list_x[i] - average_x) * (list_y[i] - average_y)
            disp_sum_down_x += (list_x[i] - average_x) ** 2
            disp_sum_down_y += (list_y[i] - average_y) ** 2
    r = disp_sum_up / ((disp_sum_down_x * disp_sum_down_y) ** 0.5)
    print("r= ", r)

    for i in range(len(list_x)):
        if copied_array[i] == 0:
            if r > 0:
                copied_array[i] = r * (list_x[i] * average_y) / average_x
            else:
                copied_array[i] = (-1 / r) * (list_x[len(list_x) - i - 1] * average_y) / average_x

    return copied_array


# восстановление числа по индексу
def recover(index, array):
    dop_index = 0
    while array[index] == None:
        if index - dop_index > 0 and array[index - dop_index] != None: array[index] = array[index - dop_index]
        if index + dop_index < len(array) and array[index + dop_index] != None:  array[index] = array[index + dop_index]
        dop_index += 1


def smoothing(array, k):
    res = []
    for i in range(len(array)): res.append(smoothing_for_element(array[:i + 1], k))
    print("Smoothing method = 2nd")
    return res


# сглаживание для 1 элемента
def smoothing_for_element(window, k):
    while math.fabs(window[-1] - (sum(window) / len(window))) / window[-1] > k: window.pop(0)
    return sum(window) / len(window)


# --------------------------------------------------------------------

def smoothing_lite(array, k):
    res = []
    a = 1
    for i in range(len(array)):
        if i < k:
            a = k - i
            res.append(smoothing_for_element_lite(array[0:i + a], k))
        else:
            res.append(smoothing_for_element_lite(array[i - k:i + a], k))
    print("Smoothing method = 1nd")
    return res


# сглаживание для 1 элемента
def smoothing_for_element_lite(window, k):
    return sum(window) / len(window)


def smoothingChoose(index, plot, k, c):
    if index == 5:
        plot = smoothing(plot, k)
    if index == 4:
        plot = smoothing_lite(plot, c)
    return plot


ticker_list = ['OGZPY', 'TATN.ME', 'SBER.ME', 'VTBR.ME', 'ALRS.ME', 'AFLT.ME', 'HYDR.ME',
               'MOEX.ME', 'NLMK.ME', 'CHMF.ME', 'DSKY.ME', 'POLY.ME', 'YNDX', 'AFKS.ME',
               'LSRG.ME', 'LSNG.ME', 'LKOH.ME', 'MTSS.ME', 'NVTK.ME', 'PIKK.ME']


# 1 Выбор тикера"
# 2 Временной период
# 3 Метод восстановления
# 4 Коэффициент
# 5 Метод сглаживания


def clicked():
    sel1 = selected.get()
    sel2 = selected2.get()
    print(sel1)
    print(sel2)

    array = {}
    plot = []
    ticker = combo_ticker.get()
    start = txt.get()
    end = txt2.get()
    print("date = ", start, end)
    data = yf.download(ticker, start=start, end=end, interval="1d")
    array[ticker] = data['Adj Close']
    for i in range(len(array[ticker])):
        plot.append(array[ticker][i])
    if sel1 == 1:
        plot = vinz(destroyer(plot, 450))
    if sel2 == 2:
        plot = approximation(destroyer(plot, 20))
    if selected == 3:
        plot2_ticker = ticker_list[1]
        if plot2_ticker == ticker:
            plot2_ticker = ticker_list[2]
        plot2 = []
        for i in range(len(array[plot2_ticker])):
            plot2.append(array[plot2_ticker][i])
        plot = correlation(destroyer(plot, 20), plot2)
    k = float(txtK.get())
    c = 5
    sm_plot = smoothingChoose(sel2, plot, k, c)
    plt.plot(plot)
    plt.show()
    plt.plot(sm_plot)
    plt.show()


from tkinter import *
from tkinter.ttk import Combobox

Iwindow = Tk()
Iwindow.title("Shares analysis")
lbl = Label(Iwindow, text="Choose token")
lbl.grid(column=0, row=0)
Iwindow.geometry('820x460')
btn = Button(Iwindow, text="Don't touch!", command=clicked)
btn.grid(column=2, row=5)

combo_ticker = Combobox(Iwindow)
combo_ticker['values'] = tuple(ticker_list)
combo_ticker.current(0)
combo_ticker.grid(column=0, row=1)

selected = IntVar()
selected2 = IntVar()

lblRecover = Label(Iwindow, text="Select method")
lblRecover.grid(column=1, row=0)
rad1 = Radiobutton(Iwindow, text='Винзовирование', value=1, variable=selected)
rad2 = Radiobutton(Iwindow, text='Линейная аппроксимация', value=2, variable=selected)
rad3 = Radiobutton(Iwindow, text='Корреляция', value=3, variable=selected)
rad1.grid(column=1, row=1)
rad2.grid(column=1, row=2)
rad3.grid(column=1, row=3)

lblSmooth = Label(Iwindow, text="Select smoothing method")
lblSmooth.grid(column=2, row=0)
rad4 = Radiobutton(Iwindow, text='Скользящее среднее', value=4, variable=selected2)
rad5 = Radiobutton(Iwindow, text='Скользящее среднее с динамическим окном', value=5, variable=selected2)
rad4.grid(column=2, row=1)
rad5.grid(column=2, row=2)

lblDate = Label(Iwindow, text="Enter Date Start")
lblDate.grid(column=1, row=4)
txt = Entry(Iwindow, width=20)
txt.grid(column=1, row=5)

lblDate = Label(Iwindow, text="Enter Date End")
lblDate.grid(column=1, row=6)
txt2 = Entry(Iwindow, width=20)
txt2.grid(column=1, row=7)

lbltxtK = Label(Iwindow, text="Enter K param")
lbltxtK.grid(column=0, row=4)
txtK = Entry(Iwindow, width=20)
txtK.grid(column=0, row=5)

Iwindow.mainloop()
