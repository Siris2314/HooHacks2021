import tkinter as tk
from tkinter import ttk
import datetime
from tkcalendar import DateEntry

root = tk.Tk()
root.resizable(True, True)

def process(startDate, endDate, ticker): 
    print(startDate, endDate, ticker)

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

root.mainloop()