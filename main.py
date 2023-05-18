import tkinter
from calendar import month_name
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, Text, END
from tkinter import messagebox
import os
from os.path import exists
from tkinter.messagebox import showinfo

import numpy
import pandas as pd
import plotly.express as px
from PIL import ImageTk,Image
import matplotlib.pyplot as plt
from datetime import datetime as dt
import datetime




# frame = tk.Frame(root, bg='grey')
# frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)
root = tk.Tk()
root.geometry('480x330')
root.resizable(False, False)
root.wm_title("Anomaly detection app")

anomaliesX = []
anomalies_ranks = []
anomaliesY = []
anonalies_date = []
anomaliesBoundUp = []
anomaliesBoundDown = []
anomaliesBoundY = []
anomalies_name = []



def filename():
    global file_name
    file_name = ""


root.after(1,filename())

def clear_all_list():
    anonalies_date.clear()
    anomaliesX.clear()
    anomalies_ranks.clear()
    anomaliesY.clear()
    anomaliesBoundY.clear()
    anomaliesBoundDown.clear()
    anomaliesBoundUp.clear()
    anomalies_name.clear()

def calculate_mean_delta(dat, date,  num):
    iterator = num
    data_out = []
    date_out = []
    while iterator < len(dat):
        data_out.append(dat[iterator] - dat[iterator-num])
        date_out.append(date[iterator])
        iterator = iterator + num
    return data_out, date_out


###############################################

class mad:
    def __init__(self, X, minMAD):
        self.X = X
        self.minMAD = numpy.float64(minMAD)
        self.MAD = 0
        self.threshold = 0
        self.isAnomaly = False
        self.degree = 0
        self.upperBound = 0
        self.lowerBound = 0

    def __calcualteMAD(self):
        self.MAD = numpy.median(numpy.abs(X - numpy.median(X)))

    def detectAnomalies(self, threshold):
        self.__calcualteMAD()
        if (self.MAD < self.minMAD):
            self.MAD = self.minMAD
        MADn = 1.4826 * self.MAD
        Z = numpy.abs(self.X[-1] - numpy.median(self.X)) / MADn
        self.upperBound = numpy.abs(numpy.median(self.X) + MADn * threshold)
        self.lowerBound = -self.upperBound
        if (Z > threshold):
            self.isAnomaly = True
            self.degree = Z // threshold

    def calculateThreshold(self):
        self.__calcualteMAD()
        if (self.MAD < self.minMAD):
            self.MAD = self.minMAD
        MADn = 1.4826 * self.MAD
        self.threshold = numpy.abs(self.X[-1] - numpy.median(self.X)) / MADn

####################################################################################################################
# ALGORYTM WOJTKA
####################################################################################################################
class qbs:
    def __init__(self, Q1, Q3, IQR, min_, max_, anomalies):
        self.Q1 = Q1
        self.Q3 = Q3
        self.IQR = IQR
        self.min_ = min_
        self.max_ = max_
        self.anomalies = []


    def calculate_parameters(self, data):
        self.Q1 = numpy.quantile(data, 0.05)
        self.Q3 = numpy.quantile(data, 0.95)
        self.IQR = self.Q3 - self.Q1
        self.max_ = (self.Q3 + 1.5 * self.IQR)
        self.min_ = (self.Q1 - 1.5 * self.IQR)

def detect_anomalies(data, window_size):
    clear_all_list()
    for i in range(0, len(data)-window_size+1, 1):
        current_data = [data [i:i+window_size] ]
        q_b_s = qbs(0,0,0,0,0,0)
        q_b_s.calculate_parameters(current_data)
        anomaliesU.append(q_b_s.max_)
        if(data[i+window_size-1] < q_b_s.min_ or data[i+window_size-1] > q_b_s.max_ and q_b_s.max_!=q_b_s.min_):
            anomaliesX.append(Y1[i + window_size-1])
            anomaliesY.append(data[i + window_size-1])
            print("Mamy anomalie w miejscu: ",i+window_size,"\nWartosc oczekiwana: <",q_b_s.min_,",",q_b_s.max_,">")
            print("Wartosc w tym miejscu: ",data[i+window_size-1],"\n")
            q_b_s.anomalies.append([i+window_size-1, current_data[0][-1]])

def runQBS_onData():
    a=4
def show_QBS():

    if (selectedw2_size.get() == ""):
        popup("Wybierz size window!")
        return
    inp3 = learning_dict[selectedw2_size.get()]
    if (file_name != ""):
        mkdir_path_QBS = mkdir_path2 + "_QBS"
        if not os.path.exists(mkdir_path_QBS):
            os.mkdir(mkdir_path_QBS)
            print("Directory ", mkdir_name, " Created ")
        else:
            print("Directory ", mkdir_name, " already exists")

        global Y1
        X1, Y1 = date_interpolation(X, X_time)
        X1, Y1 = calculate_mean_delta(X1, Y1, 1)
        global anomaliesU
        anomaliesU = []
        #X1[20000] = 0.8
        print(f"inp1={inp3}")

        detect_anomalies(X1,inp3)

        delta_usage_anomalies = plt.figure(figsize=(10, 5))

        plt.plot_date(Y1, X1, markersize=0.5, linestyle='solid')
        # plt.plot_date(anomaliesX, anomaliesY, 'ro', markersize=5)  # wyswietlanie annomalii

        for x in anomaliesX:
            colour = "red"
            plt.axvline(x, ls='-', color="red")
        #plt.plot_date(anomaliesBoundY, anomaliesBoundUp, markersize=0.5, linestyle='solid')
        plt.xlabel("date")
        plt.ylabel("Δ water usage")
        plt.tight_layout()
        plt.savefig(mkdir_path_QBS + '/1.png')

        delta_usage = plt.figure(figsize=(10, 5))
        plt.plot_date(anomaliesX, anomaliesY, 'ro', markersize=5)  # wyswietlanie annomalii
        plt.plot_date(Y1, X1, markersize=0.5, linestyle='solid')
        plt.plot_date(anomaliesBoundY, anomaliesBoundUp, markersize=0.5, linestyle='solid')
        plt.plot_date(Y1[inp3-1:], anomaliesU, markersize=0.5, linestyle='solid', color='red')
        # plt.plot_date(anomaliesBoundY, anomaliesBoundDown, markersize=0.5, linestyle='solid')
        plt.xlabel("date")
        plt.ylabel("Δ water usage")
        plt.tight_layout()
        plt.savefig(mkdir_path_QBS + '/2.png')

        usage = plt.figure(figsize=(10, 5))
        plt.plot_date(X_time, X, markersize=0.5, linestyle='solid')
        for x in anomaliesX:
            colour = "red"
            plt.axvline(x, ls='-', color=colour, alpha=0.1)
        plt.xlabel("date")
        plt.ylabel("water usage")
        plt.tight_layout()
        plt.savefig(mkdir_path_QBS + '/3.png')
        plt.show()
        popup("Dane o anomalii zapisane w folderze Pomiary")
        # f=open(mkdir_path,"w").close()
        #mkdir_path = #Pomiary/3/daty.txt
        #mkdir_path2 = #Pomiary/3
        #mkdir_path_QBS = #Pomiary/3_QBS
        mkdir_path_QBS_daty = mkdir_path_QBS +"/daty.txt"
        file_exists = exists(mkdir_path_QBS_daty)
        if (file_exists == 0):
            f = open(mkdir_path_QBS_daty, "x")
        f = open(mkdir_path_QBS_daty, 'r+')
        f.truncate(0)  # need '0' when using r+
        f = open(mkdir_path_QBS_daty, "w")
        for x in anomaliesX:
            f.write(str(x)+ "\n")
        f.close()
        print("dziala")
        anonalies_date.clear()
        print("dziala2")
    else:
        popup("Nie załadowano pliku!")

####################################################################################################################

def runMAD_onData(data, windowSize, learningWindowSize):
    threshold = 0.0
    clear_all_list()
    for i in range(0, learningWindowSize - windowSize + 1):
        X = [data[i:i + windowSize]]
        m = mad(X[0], 0.000001)
        m.calculateThreshold()
        threshold = max(m.threshold, threshold)
    threshold = 1.1 * threshold
    for i in range(learningWindowSize - windowSize + 1, len(data) - windowSize, 1):
        X = [data[i:i + windowSize]]
        m = mad(X[0], 0.001)
        m.detectAnomalies(threshold)
        anomaliesBoundUp.append(m.upperBound)
        anomaliesBoundDown.append(m.lowerBound)
        anomaliesBoundY.append(Y1[i+windowSize])
        #print('lower bound', m.lowerBound,'value', X[0][-1], 'upper bound', m.upperBound,'date', Y1[i+windowSize])
        if (m.isAnomaly == True):
            #anomaliesX.append(X_time[i + windowSize])
            anomaliesX.append(Y1[i + windowSize-1])
            anomaliesY.append(data[i + windowSize-1])
            if  m.degree < 5:
                anomalies_ranks.append(m.degree)
            else:
                anomalies_ranks.append(5)

            if (X[0][-1] > m.upperBound):
                if(m.degree < 5):
                    help = f"upper bound breach, anomaly of rank {m.degree}"
                else: help = f"upper bound breach, anomaly of rank 5"
            else:
                if(m.degree < 5):
                    help = f"lower bound breach, anomaly of rank {m.degree}"
                else: help = f"lower bound breach, anomaly of rank 5"

            anomalies_name.append(help)
            anonalies_date.append(Y1[i + windowSize])




def showMad():
    if (selectedw_size.get() == ""):
       popup("Wybierz learning size window!")
       return
    inp = learning_dict[selectedw_size.get()]
    if (selected_size.get() == ""):
        popup("Wybierz size window!")
        return
    inp2 = learning_dict[selected_size.get()]

    if (int(inp) > int(inp2)):
        popup("Learning window size musi być większe lub równe window size")
        return
    mkdir_path_mad = mkdir_path2 + "_MAD"
    print(mkdir_path_mad)
    if (file_name != ""):
        if not os.path.exists(mkdir_path_mad):
            os.mkdir(mkdir_path_mad)
            print("Directory ", mkdir_name, " Created ")
        else:
            print("Directory ", mkdir_name, " already exists")
        global Y1
        X1, Y1 = date_interpolation(X, X_time)
        X1, Y1 = calculate_mean_delta(X1, Y1, 1)



        print(f"inp1={inp}, inp2={inp2}")

        runMAD_onData(X1, int(inp), int(inp2))


        delta_usage_anomalies = plt.figure(figsize=(10, 5))

        plt.plot_date(Y1, X1, markersize=0.5, linestyle='solid')
        #plt.plot_date(anomaliesX, anomaliesY, 'ro', markersize=5)  # wyswietlanie annomalii
        colours = ['thistle', 'plum', 'violet', 'red', 'darkred']
        for x in anomaliesX:
            anomaly_rank = int(anomalies_ranks[anomaliesX.index(x)])
            colour = colours[anomaly_rank - 1]
            plt.axvline(x, ls='-', color=colour)
        #plt.plot_date(anomaliesBoundY, anomaliesBoundUp, markersize=0.5, linestyle='solid')
        plt.xlabel("date")
        plt.ylabel("Δ water usage")
        plt.tight_layout()
        plt.savefig(mkdir_path_mad+'/1.png')

        delta_usage = plt.figure(figsize=(10, 5))
        plt.plot_date(anomaliesX, anomaliesY, 'ro', markersize=5)  # wyswietlanie annomalii
        plt.plot_date(Y1, X1, markersize=0.5, linestyle='solid')
        plt.plot_date(anomaliesBoundY, anomaliesBoundUp, markersize=0.5, linestyle='solid')
        #plt.plot_date(anomaliesBoundY, anomaliesBoundDown, markersize=0.5, linestyle='solid')
        plt.xlabel("date")
        plt.ylabel("Δ water usage")
        plt.tight_layout()
        plt.savefig(mkdir_path_mad+'/2.png')

        usage = plt.figure(figsize=(10, 5))
        plt.plot_date(X_time, X, markersize=0.5, linestyle='solid')
        for x in anomaliesX:
            anomaly_rank = int(anomalies_ranks[anomaliesX.index(x)])
            colour = colours[anomaly_rank - 1]
            plt.axvline(x, ls='-', color=colour, alpha=0.1)
        plt.xlabel("date")
        plt.ylabel("water usage")
        plt.tight_layout()
        plt.savefig(mkdir_path_mad+'/3.png')
        plt.show()
        popup("Dane o anomalii zapisane w folderze Pomiary")
        # f=open(mkdir_path,"w").close()
        # mkdir_path = #Pomiary/3/daty.txt
        # mkdir_path2 = #Pomiary/3
        # mkdir_path_QBS = #Pomiary/3_QBS
        # mkdir_path_QBS_daty = #Pomiary/3_QBS/daty.txt
        mkdir_path_mad_daty = mkdir_path_mad + "/daty.txt"
        file_exists = exists(mkdir_path_mad_daty)
        if (file_exists == 0):
            f = open(mkdir_path_mad_daty, "x")
        f = open(mkdir_path_mad_daty, 'r+')
        f.truncate(0)  # need '0' when using r+
        f = open(mkdir_path_mad_daty, "w")
        for x in range(len(anonalies_date)):
            f.write(str(anonalies_date[x])+" - "+str(anomalies_name[x]) +"\n")
        f.close()
        print("dziala")
        anonalies_date.clear()
        print("dziala2")
    else:
        popup("Nie załadowano pliku!")

#   Funkcja interpolujaca
# Przyjmuje tablice z wczytanymi danymi, tablice z wczytanymi datami
# dat - dane (nie przyrosty, tylko pomiary)
# date - daty
# Zwraca: tablice z interpolowanymi danymi i datami
def date_interpolation(dat, date):
    data_out = []
    date_out = []

    deltaT_15 = datetime.timedelta(minutes=15)
    deltaT_5 = datetime.timedelta(minutes=5)
    i = 1

    delta_cal = date[i] - date[i - 1]
    if deltaT_15 - deltaT_5 < delta_cal < deltaT_15 + deltaT_5:
        print()
    else:
        i = i + 1

    while i < len(dat):
        delta_cal = date[i] - date[i - 1]
        if deltaT_15 - deltaT_5 < delta_cal < deltaT_15 + deltaT_5:
            data_out.append(dat[i])
            date_out.append(date[i])
        else:
            if delta_cal < deltaT_5:    # jesli roznica jest mala pomija jeden pomiar
                data_out[len(data_out)-1] = dat[i]
                date_out[len(date_out)-1] = date[i]
            else:
                delta_cal = round(delta_cal / deltaT_15)
                tmp_date = date_out[len(date_out)-1]
                if delta_cal != 0:
                    tmp_increase = (dat[i] - dat[i-1])/delta_cal
                else:
                    tmp_increase = 0
                j = 0
                while j < delta_cal:
                    tmp_date = tmp_date + deltaT_15     # nastepny uzupelniony pomiar
                    data_out.append(dat[i-1] + j*tmp_increase)
                    date_out.append(tmp_date)
                    j = j + 1
        i = i + 1
    return data_out, date_out


def addApp():
    global mkdir_path
    global mkdir_path2
    global mkdir_name
    global file_name
    file_name = filedialog.askopenfilename(initialdir='/', title="Select File",
                filetypes=(("Comma-separated values","*.txt"),("all files","*")))
    tmp1 = file_name.split("/")[-1]
    tmp2 = tmp1.split(".")
    mkdir_name = tmp2[0]
    mkdir_path = "Pomiary/"+mkdir_name + "/daty.txt"
    mkdir_path2 = "Pomiary/" + mkdir_name
    #print(mkdir_path)
    if not os.path.exists("Pomiary"):
        os.mkdir("Pomiary")
        print("Directory ", "Pomiary", " Created ")
    else:
        print("Directory ", "Pomiary", " already exists")
    global data
    data = pd.read_csv(file_name,';')
    global X
    X = data.values[:, 1]  # wczytanie pomiarow
    global X_time
    X_time = []
    for t in data.values[:, 0]:
        X_time.append(dt.strptime(t, '%Y-%m-%d %H:%M:%S'))  # wczytanie formatu czasu

    if file_name!="":
        addAppinfo = tkinter.Label()
        addAppinfo = tkinter.Label(text="                                                                                                                        ")
        addAppinfo.place(x=120, y=25)
        addAppinfo = tkinter.Label(text=f"Plik {tmp2[0]}.{tmp2[1]} załadowany")
        addAppinfo.place(x=120,y=25)






def show1():
    if(file_name != ""):

        #print(learning_dict[selected_size.get()])

        X1, Y1 = date_interpolation(X, X_time)
        X1, Y1 = calculate_mean_delta(X1, Y1, 1)

        usage = plt.figure(figsize=(10, 5))
        plt.plot_date(X_time, X, markersize=0.5, linestyle='solid')
        plt.xlabel("date")
        plt.ylabel("water usage")
        plt.tight_layout()
        plt.savefig('anomaly.png')
        plt.show()
    else:
        popup("Nie załadowano pliku!")


def show2():
    if(file_name != ""):

        X1, Y1 = date_interpolation(X, X_time)

        X1, Y1 = calculate_mean_delta(X1, Y1, 1)

        delta_usage = plt.figure(figsize=(10, 5))
        # plt.plot_date(anomaliesX, anomaliesY, 'ro', markersize=5)  # wyswietlanie annomalii
        plt.plot_date(Y1, X1, markersize=0.5, linestyle='solid')
        plt.xlabel("date")
        plt.ylabel("Δ water usage")
        plt.tight_layout()
        plt.show()
    else:
        popup("Nie załadowano pliku!")


def popup(text):
    messagebox.showinfo("Warning!",text)

selectedw_size = tk.StringVar()
window_size_cb = ttk.Combobox(root, textvariable=selectedw_size, width=10)

selected_size = tk.StringVar()
lerning_size_cb = ttk.Combobox(root, textvariable=selected_size, width=10)

selectedw2_size = tk.StringVar()
window2_size_cb = ttk.Combobox(root, textvariable=selectedw2_size, width=10)

lerning_size_cb['values'] = ["1 dzień", "3 dni", "1 tydzień", "2 tygodnie", "1 miesiąc", "2 miesiące", "3 miesiące", "6 miesięcy"]
lerning_size_cb['state'] = 'readonly'

window_size_cb['values'] = ["1 dzień", "3 dni", "1 tydzień", "2 tygodnie", "1 miesiąc"]
window_size_cb['state'] = 'readonly'

window2_size_cb['values'] = ["1 dzień", "3 dni", "1 tydzień", "2 tygodnie", "1 miesiąc", "2 miesiące", "3 miesiące", "6 miesięcy"]
window2_size_cb['state'] = 'readonly'

global learning_dict
learning_dict= {
    "1 dzień": 96,
    "3 dni": 288,
    "1 tydzień": 672,
    "2 tygodnie": 1344,
    "1 miesiąc": 2880,
    "2 miesiące": 5760,
    "3 miesiące": 8640,
    "6 miesięcy": 17280
}







# inputtxt = tk.Text(root, height = 1, width = 10)
# inputtxt2 = tk.Text(root, height = 1, width = 10)
inputtxt3 = tk.Text(root, height = 1, width = 10)
winSize = tkinter.Label(text="Window size")
winSize.place(x=200,y=180)
lwinSize = tkinter.Label(text="Learning window size")
lwinSize.place(x=300,y=180)
dwinSize = tkinter.Label(text="Window size")
dwinSize.place(x=200,y=240)
openFile = tk.Button(root, text= "Wczytaj plik", padx=10, pady=5,
                                        fg='white', bg='#2d305c', command=addApp)

show1 = tk.Button(root, text= "Wyswietl wykres", padx=10, pady=5,
                                        fg='white', bg='#2d305c', command=show1)
show2 = tk.Button(root, text= "Wyswietl delte", padx=10, pady=5,
                                        fg='white', bg='#2d305c', command=show2)
showMAD = tk.Button(root, text= "Algorytm MAD", padx=10, pady=5,
                                       fg='white', bg='#2d305c', command=showMad)
showQBS = tk.Button(root, text= "Algorytm QBS", padx=10, pady=5,
                                       fg='white', bg='#2d305c', command=show_QBS)

window_size_cb.pack()
window_size_cb.place(x=200,y=206.5)
window2_size_cb.pack()
window2_size_cb.place(x=200,y=266.5)
lerning_size_cb.pack()
lerning_size_cb.place(x=300,y=206.5)
openFile.pack()
openFile.place(x=20, y=20)
show1.pack()
show1.place(x=20, y=80)
show2.pack()
show2.place(x=20, y=140)
showMAD.pack()
showMAD.place(x=20, y=200)
showQBS.pack()
showQBS.place(x=20, y=260)


# inputtxt.pack()
# inputtxt.place(x=200,y=206.5)
#inputtxt2.pack()
#inputtxt2.place(x=300,y=206.5)
# inputtxt3.pack()
# inputtxt3.place(x=200,y=266.5)
  # wczytanie pliku


root.mainloop()

#TODO
#algorytm Wojtka
