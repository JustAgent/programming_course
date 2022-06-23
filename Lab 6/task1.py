from pandas import read_csv
from matplotlib import pyplot
from statsmodels.tsa.ar_model import AutoReg

data = read_csv('3.csv', header=0, index_col=0, parse_dates=True, squeeze=True)
array = data.values
print(len(array))
train, test = array, array[-50:]
print("Test Length", len(test))

window = 50
print(type(train))
model = AutoReg(train, lags=50)
model_fit = model.fit()
k = model_fit.params
print("k", k)
cache = train[len(train) - window:]
cache = [cache[i] for i in range(len(cache))]
predictions = list()
for t in range(len(test)):
    length = len(cache)
    lag = [cache[i] for i in range(length - window, length)]
    arr_predicted = k[0]
    for d in range(window):
        arr_predicted += k[d + 1] * lag[window - d - 1]
    arr_expected = test[t]
    predictions.append(arr_predicted)
    cache.append(arr_expected)
    analysis = " "
    if arr_predicted > arr_expected:
        analysis = "undervalued"
    if arr_predicted < arr_expected:
        analysis = "overvalued"
    print(f'predicted=%f, expected=%f, analysis={analysis}' % (arr_predicted, arr_expected))

pyplot.plot(test)
pyplot.plot(predictions, color='red')
pyplot.show()
