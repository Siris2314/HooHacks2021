import tkinter as tk
from tkinter import ttk
import datetime
from tkcalendar import DateEntry

from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pandas_datareader as web
import datetime as dt 


from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout,LSTM



root = tk.Tk()
root.resizable(True, True)

def stock_prediction(start_date, end_date, company):
    stock_start = start_date
    stock_end = end_date

    data = web.DataReader(str(company), 'yahoo',stock_start,stock_end)

    scalar = MinMaxScaler(feature_range=(0,1))
    scaled_data = scalar.fit_transform(data['Close'].values.reshape(-1, 1))

    prediction_past_days = 90

    x_train = []
    y_train = []

    for x in range(prediction_past_days, len(scaled_data)):
        x_train.append(scaled_data[x-prediction_past_days:x,0])
        y_train.append(scaled_data[x,0])
        
    x_train,y_train = np.array(x_train), np.array(y_train)
    x_train  = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

    model = Sequential()
    model.add(LSTM(units=50, return_sequences = True, input_shape = (x_train.shape[1],1)))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50, return_sequences = True))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50))
    model.add(Dropout(0.2))
    model.add(Dense(units=1))

    model.compile(optimizer='adam', loss="mean_squared_error")
    model.fit(x_train,y_train, epochs=25, batch_size=32)


    test_start = dt.datetime(2020,1,1)
    test_end = dt.datetime.now()

    test_data = web.DataReader(str(company), 'yahoo', test_start, test_end)
    actual_prices = test_data['Close'].values

    total_dataset = pd.concat((data['Close'], test_data['Close']), axis=0)
    model_inputs = total_dataset[len(total_dataset) - len(test_data) - prediction_past_days:].values
    model_inputs = model_inputs.reshape(-1,1)
    model_inputs = scalar.transform(model_inputs)


    x_test = []

    for x in range(prediction_past_days, len(model_inputs)):
        x_test.append(model_inputs[x-prediction_past_days:x,0])

    x_test = np.array(x_test)
    x_test = np.reshape(x_test,(x_test.shape[0], x_test.shape[1],1))

    predicted_prices = model.predict(x_test)
    predicted_prices = scalar.inverse_transform(predicted_prices)

    real_data = [model_inputs[len(model_inputs) + 1 - prediction_past_days:len(model_inputs+1), 0]]
    real_data = np.array(real_data)
    real_data = np.reshape(real_data, (real_data.shape[0], real_data.shape[1], 1))

    prediction = model.predict(real_data)
    prediction = scalar.inverse_transform(prediction)
    
    return actual_prices, predicted_prices#, (f"Prediction ${prediction}")


def process(startDate, endDate, ticker): 
    dataReal, dataPredict = stock_prediction(startDate, endDate, ticker)

    fig = Figure()
    #y = [i**1 for i in range(101)]

    plot1 = fig.add_subplot(111)
    plot2 = fig.add_subplot(111)

    plot1.plot(dataReal, color="red", label="Actual Price")
    plot2.plot(dataPredict, color="green", label="Predicted Price")


    canvas = FigureCanvasTkAgg(fig, master = root)
    canvas.draw()

    canvas.get_tk_widget().grid(row = 7, column = 3)

    toolbar = NavigationToolbar2Tk(canvas, root)
    toolbar.update()

    canvas.get_tk_widget().grid(row = 10, column = 3)


def showUI():
    # dates
    ttk.Label(root, text = 'Choose the Period').grid(row = 1, column = 0)
    # calendar object cant have .grid after the initialization, changes the object 
    # to a 'NoneType'
    deStart = DateEntry(root, width = 12)
    deStart.grid(row = 2, column = 0)
    
    deEnd = DateEntry(root, width = 12)
    deEnd.grid(row = 2, column = 1)

    ttk.Label(root, text = "Enter Ticker").grid(row = 4, column = 0)
    tickerE = tk.Entry(root)
    tickerE.grid(row = 4, column = 1)


    def getAllInputs() :
        dateStart = deStart.get_date()
        dateEnd = deEnd.get_date()
        ticker = tickerE.get()
        return dateStart, dateEnd, ticker
    
    def submit():
        startDate, endDate, ticker = getAllInputs()
        process(startDate, endDate, ticker)

    button1 = tk.Button(root, text = 'submit', command = submit).grid(row = 5, column = 0)

showUI()

#stock_prediction(dt.datetime(2020, 1, 1), dt.datetime(2021, 1, 1), 'AAPL')

root.mainloop()