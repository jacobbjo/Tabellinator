__author__ = 'Jacob'
__copyright__ = "May 2015"

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
import tkinter.scrolledtext as tkst
import sys
from tkinter import ttk   # "css for tkinter" - to make things less win95
from functions import *
from Train import Train
LARGE_FONT = ("Verdana", 13)
LARGE_FONT_TITLE = ("Verdana", 13, "bold", "underline")
MEDIUM_FONT = ("Verdana", 11, "bold")
SMALL_FONT = ("Verdana", 9)


class TrainApp(tk.Tk):
    """
    Container class for an tkinter instance of the "Tabellinator" app
    """

    def __init__(self, *args, **kwargs):
        """
        Creates a an tkinter instance of the "Tabellinator" app with a container for pages for

        :param inputStations: A list of lists containing station name and distance from the start station in km
        :param train: A train object to specify train acceleration
        :param waitTime: int > 1 [minutes]
                     The time the train waits on each station, up to. for example = 1 gives times between 0-60 seconds
                     according to assignment specification
        :param waitTimeEnd: datetime.timedelta > 60 seconds
                        The time the train waits on the end stations.
        :param startTime: A datetime.timedelta object to specify the departure time for the first train
        :param endTime: A datetime.timedelta object to specify the departure time for the last train from the last station
        :param trainAm: int >= 0 The amount of trains that travels the line on weekdays
        :param trainAmWkd: int >= 0 The amount of trains that travels the line on weekdays

        """
        # Setting up tkinter window
        tk.Tk.__init__(self)
        #tk.Tk.iconbitmap(self, default="icon.ico")
        tk.Tk.wm_title(self, "Tabellinator")

        # Setting up variables
        self.inputStations = []
        self.train = Train(1, 1, 1)
        self.waitTime = 0
        self.waitTimeEnd = 0
        self.startHour = 0
        self.startMinute = 0
        self.endHour = 0
        self.endMinute = 0
        self.trainAm = 0
        self.trainAmWkd = 0
        self.loaded = False
        fileRead = False
        self.errorMessage = tk.StringVar()

        # Loading from file, handling errors and creating stations
        try:
            self.inputStations, self.train, self.waitTime, self.waitTimeEnd, self.startHour, self.startMinute, \
                self.endHour, self.endMinute, self.trainAm, self.trainAmWkd = readFile("tag.txt")
            fileRead = True
        except FileNotFoundError:
            self.errorMessage.set("Filen tag.txt hittades inte")
        #except:
        #    self.errorMessage.set("Filen har fel format eller något saknas"
        #                          "\nRätta till filen och starta om programmet")
        try:
            if fileRead:
                self.stations = createStations(self.inputStations, self.train, self.waitTime, self.waitTimeEnd,
                                               self.startHour, self.startMinute, self.endHour, self.endMinute,
                                               self.trainAm, self.trainAmWkd)
                self.loaded = True
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.errorMessage.set("Fel vid inläsning av filen:\n" + str(exc_value))

        # Setting up container frame
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, DisplayPage, SettingsPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        """
        Brings a page for the app to the front so it's intractable
        :param cont: the container for which to bring a page to the front
        """
        frame = self.frames[cont]
        frame.tkraise()

    def getStation(self, search):
        """
        Search method to find a station in a station list
        :param search:
        :return: returns the station object if found, otherwise none
        """
        for object in self.stations:
            if object.name.lower() == search:
                return object
        return None


class StartPage(tk.Frame):
    """
    A frame class for the startpage to be put in the container
    """

    def __init__(self, parent, controller):
        """
        initialises a frame class for the startpage to be put in the container
        """
        tk.Frame.__init__(self, parent)

        # Creating Labels
        self.labelVarStations = tk.StringVar()
        labelTitle = ttk.Label(self, text="Välkommen till tågtidtabellskaparen\nTabellinator", font=LARGE_FONT)
        labelErrorTitle = ttk.Label(self, text="Fel på indatafilen", font=LARGE_FONT_TITLE, foreground="Red")
        labelError = ttk.Label(self, textvariable=controller.errorMessage, font=SMALL_FONT, foreground="Red")
        labelLoaded = ttk.Label(self, text="Inlästa stationer:", font=MEDIUM_FONT)
        labelStations = ttk.Label(self, textvariable=self.labelVarStations, font=SMALL_FONT)
        labelTitle.pack(pady=10, padx=10)

        buttonDisplayPage = ttk.Button(self, text="Visa tabell",
                            command=lambda: controller.show_frame(DisplayPage))
        buttonSettingsPage = ttk.Button(self, text="Inställningar",
                            command=lambda: controller.show_frame(SettingsPage))

        # Presents different start pages depending on if the input file is correct
        if controller.loaded:
            stationNameList = ""
            for station in controller.stations:
                stationNameList += (station.name + "\n")
            self.labelVarStations.set(stationNameList)
            labelLoaded.pack(pady=10)
            labelStations.pack()
            buttonDisplayPage.pack()
            buttonSettingsPage.pack()

        else:
            labelErrorTitle.pack(pady=10, padx=10)
            labelError.pack(pady=10, padx=10)


class DisplayPage(tk.Frame):
    """
    A frame class for the display page to be put in the container
    """

    def __init__(self, parent, controller):
        """
        initialises a frame class for the display page to be put in the container
        """
        tk.Frame.__init__(self, parent)
        try:
            startStation = controller.stations[0].name
            endStation = controller.stations[len(controller.stations) - 1].name
        except:
            startStation = "startstation"
            endStation = "slutstation"

        labelTitle = ttk.Label(self, text ="Sök station:", font=LARGE_FONT_TITLE)
        labelTitle.grid(row=0, column=0, columnspan=4, pady=10, padx=10)

        # Creates a search entry and a button
        search = tk.StringVar()
        self.searchBox = ttk.Entry(self, textvariable=search)
        buttonSearch = ttk.Button(self, text="Sök!", command=lambda: self.makeSearch(self.searchBox, controller))

        # Puts search entry and the button on the grid
        self.searchBox.grid(row=1, column=1, columnspan=2, pady=5, padx=5)
        buttonSearch.grid(row=2, column=1, columnspan=2, pady=5, padx=5)

        self.stationName = tk.StringVar()
        labelName = ttk.Label(self, textvariable=self.stationName, font=LARGE_FONT)
        labelName.grid(row=3, column=1, columnspan=2)

        # Creates labels for scroll lists
        labelScr1 = ttk.Label(self, text ="Avg. mot \n" + endStation + ":", font=SMALL_FONT)
        labelScr2 = ttk.Label(self, text ="Avg. mot \n" + startStation + ":", font=SMALL_FONT)
        labelScr3 = ttk.Label(self, text ="Avg. mot \n" + endStation + " helg:", font=SMALL_FONT)
        labelScr4 = ttk.Label(self, text ="Avg. mot \n" + startStation + " helg:", font=SMALL_FONT)

        # Puts the labels on the grid
        labelScr1.grid(row=4, column=0)
        labelScr2.grid(row=4, column=1)
        labelScr3.grid(row=4, column=2)
        labelScr4.grid(row=4, column=3)

        # Creates scroll lists
        self.scrolledResult1 = tkst.ScrolledText(self, wrap='word', width=9, height=20)
        self.scrolledResult2 = tkst.ScrolledText(self, wrap='word', width=9, height=20)
        self.scrolledResult3 = tkst.ScrolledText(self, wrap='word', width=9, height=20)
        self.scrolledResult4 = tkst.ScrolledText(self, wrap='word', width=9, height=20)

        # Puts scroll lists on the grid
        self.scrolledResult1.grid(row=5, column=0)
        self.scrolledResult2.grid(row=5, column=1)
        self.scrolledResult3.grid(row=5, column=2)
        self.scrolledResult4.grid(row=5, column=3)

        # Creates navigational buttons
        buttonSettings = ttk.Button(self, text="Inställningar", command=lambda: controller.show_frame(SettingsPage))
        buttonStart = ttk.Button(self, text="Start", command=lambda: controller.show_frame(StartPage))

        # Puts navigational buttons on the grid
        buttonSettings.grid(row=6, column=2)
        buttonStart.grid(row=6, column=3)

    def makeSearch(self, entry, controller):
        """
        Runs when the search-button is pressed
        :param entry: string, entry from the search entry
        """
        search = entry.get().lower()
        station = controller.getStation(search)
        self.scrolledResult1.delete('1.0', tk.END)
        self.scrolledResult2.delete('1.0', tk.END)
        self.scrolledResult3.delete('1.0', tk.END)
        self.scrolledResult4.delete('1.0', tk.END)
        self.stationName.set("")

        if station is not None:
            departuresFromStart = station.departuresFromStartStr()
            departuresFromEnd = station.departuresFromEndStr()
            departuresFromStartWkd = station.departuresFromStartWkdStr()
            departuresFromEndWkd = station.departuresFromEndWkdStr()

            self.scrolledResult1.insert('insert', departuresFromStart)
            self.scrolledResult2.insert('insert', departuresFromEnd)
            self.scrolledResult3.insert('insert', departuresFromStartWkd)
            self.scrolledResult4.insert('insert', departuresFromEndWkd)
            self.stationName.set("Avgångar från " + station.name + ":")
        else:
            if len(search) > 1:
                self.searchBox.delete('0', tk.END)
                self.searchBox.insert('insert', "Stationen hittades ej!")


class SettingsPage(tk.Frame):
    """
    A frame class for the settings page to be put in the container
    """

    def __init__(self, parent, controller):
        """
        initialises a frame class for the settings page to be put in the container
        """
        tk.Frame.__init__(self, parent)
        # Getting station names:
        try:
            startStation = controller.stations[0].name
            endStation = controller.stations[len(controller.stations) - 1].name
        except AttributeError:
            startStation = "startstation"
            endStation = "slutstation"

        # Creating Labels
        labelTitle = ttk.Label(self, text="Inställningar", font=LARGE_FONT_TITLE)
        labelTitleTrain = ttk.Label(self, text="Tågprestanda: ", font=MEDIUM_FONT)
        self.labelAcc = ttk.Label(self, text="Acceleration\n(0.4-0.8 m/s^2):", font=SMALL_FONT)
        self.labelRet = ttk.Label(self, text="Retardation\n(1.2-2.0 m/s^2):", font=SMALL_FONT)
        self.labelMax = ttk.Label(self, text="Maxhastighet\n(30-45 m/s):", font=SMALL_FONT)
        labelTitleTrainAm = ttk.Label(self, text="Tåg i trafik: ", font=MEDIUM_FONT)
        self.labelTrainAm = ttk.Label(self, text="Vardagar (min 1):", font=SMALL_FONT)
        self.labelTrainAmWkd = ttk.Label(self, text="Helger (min 1):", font=SMALL_FONT)
        labelTitleTimes = ttk.Label(self, text="Avgångstider: ", font=MEDIUM_FONT)
        self.labelHours = ttk.Label(self, text="Timme (0-23): ", font=SMALL_FONT)
        self.labelMinutes = ttk.Label(self, text="Minut (0-59): ", font=SMALL_FONT)
        self.labelFirstDep = ttk.Label(self, text="Första avgången \nfrån " + startStation + " :", font=SMALL_FONT)
        self.labelLastDep = ttk.Label(self, text="Sista avgången \nfrån " + endStation + " senast:", font=SMALL_FONT)
        labelTitleWait = ttk.Label(self, text="Väntetider: ", font=MEDIUM_FONT)
        self.labelWait = ttk.Label(self, text="Vid alla stationer\nupp till(1-59 min):", font=SMALL_FONT)
        self.labelWaitEnd = ttk.Label(self, text="Vid vändstationer\n(1-59 min):", font=SMALL_FONT)
        self.savedTime = tk.StringVar("")
        self.labelSavedTime = ttk.Label(self, textvariable=self.savedTime, font=SMALL_FONT)

        # Putting labels on grid
        labelTitle.grid(row=0, column=0, columnspan=3, pady=10)
        labelTitleTrain.grid(row=1, column=0, columnspan=3, pady=10)
        self.labelAcc.grid(row=2, column=0, sticky="w")
        self.labelRet.grid(row=2, column=1, sticky="w")
        self.labelMax.grid(row=2, column=2, sticky="w")
        labelTitleTrainAm.grid(row=4, column=0, columnspan=3, pady=10)
        self.labelTrainAm.grid(row=5, column=0, sticky="w")
        self.labelTrainAmWkd.grid(row=5, column=1, sticky="w")
        labelTitleTimes.grid(row=7, column=0, columnspan=3, pady=10)
        self.labelHours.grid(row=8, column=1, sticky="w")
        self.labelMinutes.grid(row=8, column=2, sticky="w")
        self.labelFirstDep.grid(row=9, column=0, sticky="w")
        self.labelLastDep.grid(row=10, column=0, sticky="w")
        labelTitleWait.grid(row=11, column=0, columnspan=3, pady=10)
        self.labelWait.grid(row=12, column=0, sticky="w")
        self.labelWaitEnd.grid(row=12, column=1, sticky="w")
        self.labelSavedTime.grid(row=14, column=1, sticky="e")

        # Creating StingVars for Entries
        self.entryTextAcc = tk.StringVar()
        self.entryTextRet = tk.StringVar()
        self.entryTextMax = tk.StringVar()
        self.entryTextTrains = tk.StringVar()
        self.entryTextTrainsWkd = tk.StringVar()
        self.entryTextFirstDepHour = tk.StringVar()
        self.entryTextFirstDepMinute = tk.StringVar()
        self.entryTextLastDepHour = tk.StringVar()
        self.entryTextLastDepMinute = tk.StringVar()
        self.entryTextWait = tk.StringVar()
        self.entryTextWaitEnd = tk.StringVar()

        # Correcting time values
        if controller.endHour == 24 and controller.endMinute == 0:
            endHour = 0
        else:
            endHour = controller.endHour

        # Setting StringVars from file inputs
        self.entryTextAcc.set(str(controller.train.acceleration))
        self.entryTextRet.set(str(controller.train.retardation))
        self.entryTextMax.set(str(controller.train.maxSpeed))
        self.entryTextTrains.set(str(controller.trainAm))
        self.entryTextTrainsWkd.set(str(controller.trainAmWkd))
        self.entryTextFirstDepHour.set(str(controller.startHour))
        self.entryTextFirstDepMinute.set(str(controller.startMinute))
        self.entryTextLastDepHour.set(str(endHour))
        self.entryTextLastDepMinute.set(str(controller.endMinute))
        self.entryTextWait.set(str(controller.waitTime))
        self.entryTextWaitEnd.set(str(controller.waitTimeEnd))

        # Creating Entry Fields
        self.entryAcc = ttk.Entry(self, textvariable=self.entryTextAcc)
        self.entryRet = ttk.Entry(self, textvariable=self.entryTextRet)
        self.entryMax = ttk.Entry(self, textvariable=self.entryTextMax)
        self.entryTrains = ttk.Entry(self, textvariable=self.entryTextTrains)
        self.entryTrainsWkd = ttk.Entry(self, textvariable=self.entryTextTrainsWkd)
        self.entryFirstDepHour = ttk.Entry(self, textvariable=self.entryTextFirstDepHour)
        self.entryFirstDepMinute = ttk.Entry(self, textvariable=self.entryTextFirstDepMinute)
        self.entryLastDepHour = ttk.Entry(self, textvariable=self.entryTextLastDepHour)
        self.entryLastDepMinute = ttk.Entry(self, textvariable=self.entryTextLastDepMinute)
        self.entryWait = ttk.Entry(self, textvariable=self.entryTextWait)
        self.entryWaitEnd = ttk.Entry(self, textvariable=self.entryTextWaitEnd)

        # Putting Entry Fields on grid
        self.entryAcc.grid(row=3, column=0, sticky="w")
        self.entryRet.grid(row=3, column=1, sticky="w")
        self.entryMax.grid(row=3, column=2, sticky="w")
        self.entryTrains.grid(row=6, column=0, sticky="w")
        self.entryTrainsWkd.grid(row=6, column=1, sticky="w")
        self.entryFirstDepHour.grid(row=9, column=1, sticky="w")
        self.entryFirstDepMinute.grid(row=9, column=2, sticky="w")
        self.entryLastDepHour.grid(row=10, column=1, sticky="w")
        self.entryLastDepMinute.grid(row=10, column=2, sticky="w")
        self.entryWait.grid(row=13, column=0, sticky="w")
        self.entryWaitEnd.grid(row=13, column=1, sticky="w")

        # Creating buttons
        buttonSave = ttk.Button(self, text="Spara", command=lambda: self.saveEntries(controller))
        buttonHome = ttk.Button(self, text="Start", command=lambda: controller.show_frame(StartPage))
        buttonDisp = ttk.Button(self, text="Visa tabell", command=lambda: controller.show_frame(DisplayPage))

        # Putting buttons on grid
        buttonSave.grid(row=14, column=2)
        buttonHome.grid(row=15, column=0)
        buttonDisp.grid(row=15, column=1)

    def convertTime(self, timeObj):
        """
        Converts a datetime.timedelta to ints of the hours and minutes
        :param timeObj: a datetime.timedelta
        :return: hours: int, amount of hours
                 minutes: int, amount of minutes
        """
        hours, rem = divmod(timeObj.seconds, 3600)
        minutes, seconds = divmod(rem, 60)
        return hours, minutes

    def saveEntries(self, controller):
        """
        Saves entries to the controller and creates new stations, based on the new values

        """
        #fileStations, train, waitTime, waitTimeEnd, startHour, startMinute, endHour, endMinute, trainAm, trainAmWkd
        trainAcc = self.tryFloatEntry(self.entryAcc, self.labelAcc, 0.4, 0.8)
        trainRet = self.tryFloatEntry(self.entryRet, self.labelRet, 1.2, 2)
        trainMax = self.tryFloatEntry(self.entryMax, self.labelMax, 30, 45)
        waitTime = self.tryIntEntry(self.entryWait, self.labelWait, 1, 59)
        waitTimeEnd = self.tryIntEntry(self.entryWaitEnd, self.labelWaitEnd, 1, 59)
        startHour = self.tryIntEntry(self.entryFirstDepHour, self.labelFirstDep, 0, 23)
        startMinute = self.tryIntEntry(self.entryFirstDepMinute, self.labelFirstDep, 0, 59)
        endHour = self.tryIntEntry(self.entryLastDepHour, self.labelLastDep, 0, 23)
        endMinute = self.tryIntEntry(self.entryLastDepMinute, self.labelLastDep, 0, 59)
        trainAm = self.tryIntEntry(self.entryTrains, self.labelTrainAm, 1)
        trainAmWkd = self.tryIntEntry(self.entryTrainsWkd, self.labelTrainAmWkd, 1)

        # Correcting 00:00 to 24 hours
        if endHour == 0 and endMinute == 0:
            endHour = 24

        try:
            controller.stations = createStations(controller.inputStations, Train(trainAcc, trainRet, trainMax), waitTime, waitTimeEnd, startHour, startMinute, endHour, endMinute, trainAm, trainAmWkd)
            self.labelMinutes.config(foreground="black")
            self.labelHours.config(foreground="black")
            self.savedTime.set("Sparat: " + str(datetime.datetime.now().time().strftime("%H:%M:%S")))
        except IOError:
            self.labelFirstDep.config(foreground="red")
            self.entryFirstDepHour.config(foreground="red")
            self.entryFirstDepMinute.config(foreground="red")
            self.labelLastDep.config(foreground="red")
            self.entryLastDepHour.config(foreground="red")
            self.entryLastDepMinute.config(foreground="red")
            self.labelMinutes.config(foreground="red")
            self.labelHours.config(foreground="red")
        except:
            pass

    def tryFloatEntry(self, entry, label, lower, upper):
        """
        Tries if a value is in the given parameters, if not: turns entry and label red and raises ValueError
        :param entry: entry object to get information from and control color of
        :param label: label object to control color of
        :param lower: float, lower limit to try for
        :param upper: float, upper limit to try for
        :return: floatValue, float, the input to the entry field as a float
        """
        try:
            floatValue = float(entry.get().replace(",", "."))
            if not lower <= floatValue <= upper:
                raise ValueError
            label.config(foreground="black")
            entry.config(foreground="black")
            return floatValue
        except ValueError:
            label.config(foreground="red")
            entry.config(foreground="red")

    def tryIntEntry(self, entry, label, lower, upper=None):
        """
        Tries if a value is in the given parameters, if not: turns entry and label red and raises ValueError
        :param entry: entry object to get information from and control color of
        :param label: label object to control color of
        :param lower: int, lower limit to try for
        :param upper: int, upper limit to try for
        :return: value, int, the input to the entry field as a float
        """
        try:
            value = int(entry.get())
            if upper is None:
                if value < lower:
                    raise ValueError
            else:
                if not lower <= value <= upper:
                    raise ValueError
            label.config(foreground="black")
            entry.config(foreground="black")
            return value
        except ValueError:
            label.config(foreground="red")
            entry.config(foreground="red")

