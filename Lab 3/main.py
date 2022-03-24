import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np


def is_digit(string):  # Проверка на число
    if string.isdigit():
        return True
    else:
        try:
            float(string)
            return True
        except ValueError:
            return False


def deleteNan(array):  # Удаляем nan в листах
    fix_array = []
    for i in range(len(array)):
        if array[i] > 0:
            fix_array.append(array[i])

    return fix_array


def correlation(array, array2):  # находим кэф коррелляции
    list_y = []
    list_x = []
    sum_x = 0
    sum_y = 0
    ln1 = len(array)
    ln2 = len(array2)
    ln = min(ln1, ln2)
    for i in range(ln):
        if array[i] > 0:
            if array2[i] > 0:
                list_y.append(array[i])
                list_x.append(array2[i])
            else:
                array2[i] = array2[i - 1]
        else:
            array[i] = array[i - 1]
            if array2[i] > 0:
                list_y.append(array[i])
                list_x.append(array2[i])
            else:
                array2[i] = array2[i - 1]
                list_y.append(array[i])
                list_x.append(array2[i])
    sum_x += sum(list_x)
    sum_y += sum(list_y)
    average_x = sum_x / (len(list_x))
    average_y = sum_y / (len(list_y))
    disp_sum_up = 0
    disp_sum_down_x = 0
    disp_sum_down_y = 0

    for i in range(len(list_x)):
        if list_y[i] != 0:
            disp_sum_up += (list_x[i] - average_x) * (list_y[i] - average_y)
            disp_sum_down_x += (list_x[i] - average_x) ** 2
            disp_sum_down_y += (list_y[i] - average_y) ** 2
    r = disp_sum_up / ((disp_sum_down_x * disp_sum_down_y) ** 0.5)

    return r


# ticker_list = ['OGZPY', 'TATN.ME', 'SBER.ME']  # , 'VTBR.ME']
ticker_list = ['OGZPY', 'TATN.ME', 'SBER.ME', 'VTBR.ME', 'ALRS.ME', 'AFLT.ME', 'HYDR.ME',
               'MOEX.ME', 'NLMK.ME', 'CHMF.ME', 'DSKY.ME', 'POLY.ME', 'YNDX', 'AFKS.ME',
               'LSRG.ME', 'LSNG.ME', 'LKOH.ME', 'MTSS.ME', 'NVTK.ME', 'PIKK.ME']
st = 60
array = {}
volume = {}
anatoliy_sum = 10000000
boris_sum = 10000000
evgeniy_sum = 10000000
anatoliy = {}
boris = {}
evgeniy = {}

for ticker in ticker_list:
    anatoliy[ticker] = 0
    boris[ticker] = 0
    evgeniy[ticker] = 0
    data = yf.download(ticker, start="2017-01-01", end="2019-12-31", interval="1d")
    volume[ticker] = data['Volume']
    array[ticker] = data['Adj Close']
    array[ticker] = deleteNan(array[ticker])

for month in range(12):  # Для всех лет

    results1 = {}
    results0 = {}
    start = st * month
    end = start + 60

    for ticker in ticker_list:
        anatoliy_sum += anatoliy[ticker] * array[ticker][end]
        anatoliy[ticker] = 0
        boris_sum += boris[ticker] * array[ticker][end]
        boris[ticker] = 0
        # Евгеха
        evgeniy_sum += evgeniy[ticker] * array[ticker][end]
        evgeniy[ticker] = 0
        #print(evgeniy_sum)
    for i in range(0, len(ticker_list) - 1):  # Берем первый элемент списка тикеров
        temp_arr1 = []
        for h in range(start, end):
            temp_arr1.append(array[ticker_list[i]][h])
        for j in range(i + 1, len(ticker_list)):  # Находим корр первого с каждым следующим
            temp_arr2 = []
            for h in range(start, end):
                temp_arr2.append(array[ticker_list[j]][h])
            r = correlation(temp_arr1, temp_arr2)
            results1[r] = (ticker_list[i], ticker_list[j])
            results0[abs(r)] = (ticker_list[i], ticker_list[j])
    #print(results1)   # Посмотретьь котировки ( их 4560 )
    # Сортировка r
    sorted_results1 = list(results1)
    sorted_results1 = sorted(sorted_results1)
    sorted_results1.reverse()
    sorted_results0 = list(results0)
    sorted_results0 = sorted(sorted_results0)

    # Этап вложения
    for i in range(3):
        anatoliy[results1[sorted_results1[i]][0]] += (anatoliy_sum / 6) / array[results1[sorted_results1[i]][0]][end]
        anatoliy[results1[sorted_results1[i]][1]] += (anatoliy_sum / 6) / array[results1[sorted_results1[i]][1]][end]
        boris[results0[sorted_results0[i]][0]] += (boris_sum / 6) / array[results0[sorted_results0[i]][0]][end]
        boris[results0[sorted_results0[i]][1]] += (boris_sum / 6) / array[results0[sorted_results0[i]][1]][end]
    anatoliy_sum = 0
    boris_sum = 0
    # Евгений---------------------------------------------------
    total_value_sum = 0
    for ticker in ticker_list:
        total_value_sum += volume[ticker][end]
    for ticker in ticker_list:
        evgeniy[ticker] = (evgeniy_sum * (volume[ticker][end] / total_value_sum)) * 5.4 / (
                array[ticker][end] * array[results1[sorted_results1[0]][0]][end])
    evgeniy_sum = 0

# Убираем оставшиеся акции
for ticker in ticker_list:
    anatoliy_sum += anatoliy[ticker] * array[ticker][-1]
    anatoliy[ticker] = 0
    boris_sum += boris[ticker] * array[ticker][-1]
    boris[ticker] = 0
    evgeniy_sum += evgeniy[ticker] * volume[ticker][-1]
    evgeniy[ticker] = 0
print(anatoliy_sum, boris_sum, evgeniy_sum)
