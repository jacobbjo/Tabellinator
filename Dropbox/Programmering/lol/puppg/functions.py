__author__ = 'Jacob'
__copyright__ = "May 2015"
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from Train import Train
from Station import Station

def readFile(file):
    """
    Takes a file following a certain model where === separates the paragraphs, reads the lines in each paragraph and
    returns them with the proper object types for createStations()

    If any value is outside of the specifications it raises a ValueError

    :param file: Specifies the file name or file path from which to import data.
    :return: inputStations: A list of lists containing station name and distance from the start station in km
             train: A train object to specify train acceleration
             waitTime: int > 1 [minutes]
                       The time the train waits on each station, up to. for example = 1 gives times between 0-60 seconds
                       according to assignment specification
             waitTimeEnd: datetime.timedelta > 60 seconds
                          The time the train waits on the end stations.
             startTime: A datetime.timedelta object to specify the departure time for the first train
             endTime: A datetime.timedelta object to specify the departure time for the last train from the last station
             trainAm: int >= 0 The amount of trains that travels the line on weekdays
             trainAmWkd: int >= 0 The amount of trains that travels the line on weekdays
    """

    fileStations = []
    fil = open(file, "r", encoding='utf-8', errors='ignore')
    paragraph = 0
    for line in fil:
        if "===" in line:
            paragraph += 1
            continue
        if paragraph == 1:

            trainAcc, trainRet, trainMax = float(line.split()[0]), float(line.split()[1]), float(line.split()[2])
            train = Train(trainAcc, trainRet, trainMax)
        elif paragraph == 3:
            startHour, startMinute, endHour, endMinute = int(line.split()[0].split(":")[0]), \
                                                    int(line.split()[0].split(":")[1]), \
                                                    int(line.split()[1].split(":")[0]), \
                                                    int(line.split()[1].split(":")[1])
            if endHour == 0 and endMinute == 0:
                endHour = 24

        elif paragraph == 5:
            trainAm, trainAmWkd = int(line.split()[0]),\
                                int(line.split()[1])
        elif paragraph == 7:
            waitTime, waitTimeEnd = int(line.split()[0]), int(line.split()[1])

        elif paragraph == 9:
            name = line.split()[0]
            distance = float(line.split()[1])
            fileStations.append([name, distance])

    fil.close()
    return fileStations, train, waitTime, waitTimeEnd, startHour, startMinute, endHour, endMinute, trainAm, trainAmWkd

def makeTable (start, end, trains, travel, wait):
    """
    Makes a timetable for a station with a given start time, end time, amount of trains, travel time and wait time
    The returned timetable will have an even dispersion of times depending on the amount of trains.

    Raises IOError if the train can't even travel one time (end time < (start time + travel time + wait time)

    :param start: A datetime.timedelta object describing when the first train departures
    :param end: A datetime.timedelta object describing when the last train should departures
    :param trains: The amount of trains that go back and forth on the line
    :param travel: A datetime.timedelta object describing the total travel time for the line
    :param wait: A datetime.timedelta object describing the wait-time and the turning stations
    :return: table: A list of datetime.timedelta objects for every departure from the station
    """
    if end < (start + travel + wait):
        raise IOError("The end time for the line can not be less than: \nstart time + travel time + wait time")

    table = []
    dispersion = (travel + wait)/trains
    # Rounding to a minute
    dispersionRound = (dispersion.seconds // 60) + 1
    time = start
    while time < end - (travel/2):
        table.append(time)
        time += datetime.timedelta(minutes=dispersionRound)
    return table

def setDepartureTimes(list, station):
    """
    Makes a timetable for each direction for a given station based on the timetable list for the station

    :param list: a list of datetime.timedelta objects for every departure from the station
    :param station: a Station object for which to make the table
    :return: depFromStartList: A list of datetime.timedelta objects for every departure towards end station
             depFromEndList A list of datetime.timedelta objects for every departure towards the start station
    """
    depFromStartList = []
    depFromEndList = []
    for i in list:
        depFromStart = station.timeFromStart + i
        depFromEnd = station.timeFromEnd + i

        if depFromStart > datetime.timedelta(hours=24):
            depFromStart -= datetime.timedelta(hours=24)

        if depFromEnd > datetime.timedelta(hours=24):
            depFromEnd -= datetime.timedelta(hours=24)

        depFromStartList.append(depFromStart)
        depFromEndList.append(depFromEnd)

    return depFromStartList, depFromEndList

def verifyValues(fileStations, train, waitTime, waitTimeEnd, startHour, startMinute, endHour, endMinute,
                 trainAm, trainAmWkd):
    """
    Verifying that all the values are according to the specifications of the application

    :param fileStations: A list of lists containing station name and distance from the start station in km
    :param train: A train object to specify train acceleration
    :param waitTime: int > 1 [minutes]
                     The time the train waits on each station, up to. for example = 1 gives times between 0-60 seconds
                     according to assignment specification
    :param waitTimeEnd: int, The time the train waits on the end stations.
    :param startHour: int, specify the departure hour for the first train
    :param startMinute: int, specify the departure minute for the first train
    :param endHour: int, specify the departure hour for the last train from the last station
    :param endMinute: int, specify the departure minute for the last train from the last station
    :param trainAm: int >= 0 The amount of trains that travels the line on weekdays
    :param trainAmWkd: int >= 0 The amount of trains that travels the line on weekdays
    :return:
    """
    i = 0
    # Verifying stations
    for station in fileStations:
        i += 1
        # Verifying that the station name is not longer that 15 char
        if len(station[0]) < 1:
            raise ValueError("Ett stationsnamn är för kort")
        if len(station[0]) > 15:
            raise ValueError("Ett stationsnamn är för långt")
        # Verifying that the distance to the station is not negative:
        if station[1] < 0:
            raise ValueError("Avståndet till en station kan inte vara negativt")
        # Verifying that the station before does not have the same or greater distance to start station
        if (i > 1) and (station[1] <= (fileStations[i - 2][1])):
            print(station[1])
            print(fileStations[i - 1][1])
            raise ValueError("Efterföljande station kan inte ha kortare avstånd till startstationen")

    # Verifying Train values
    if train.acceleration < 0.4 or train.acceleration > 0.8:
        raise ValueError("Tågets accelerationsvärde är utanför gränserna")
    if train.retardation < 1.2 or train.retardation > 2:
        raise ValueError("Tågets retardationsvärde är utanför gränserna")
    if train.maxSpeed < 30 or train.maxSpeed > 45:
        raise ValueError("Tågets maxhastighetsvärde är utanför gränserna")

    # Verifying wait values
    if waitTime < 1 or waitTime > 59:
        raise ValueError("Väntetiden vid varje station är utanför gränserna")
    if waitTimeEnd < 1 or waitTimeEnd > 59:
        raise ValueError("Väntetiden vid vändstationerna är utanför gränserna")

    # Verifying start and end times
    if startHour > 23 or startHour < 0 or startMinute > 59 or startMinute < 0:
        if not startHour == 24 and startMinute == 0:
            raise ValueError("Starttiden är ogiltig")
    if endHour > 23 or endHour < 0 or endMinute > 59 or endMinute < 0:
        if not endHour == 24 and endMinute == 0:
            raise ValueError("Sluttiden är ogiltig ")

    # Verifying train amounts
    if trainAm < 1:
        raise ValueError("Antalet tåg på vardagar måste vara minst 1")
    if trainAmWkd < 1:
        raise ValueError("Antalet tåg på helger måste vara minst 1")

    # If all checks passed, returns true
    return True

def createStations(fileStations, train, waitTime, waitTimeEndIn, startHourIn, startMinuteIn, endHourIn, endMinuteIn,
                   trainAm, trainAmWkd):
    """
    Creates a list of station objects with all it's departure times in each direction.

    :param fileStations: A list of lists containing station name and distance from the start station in km
    :param train: A train object to specify train acceleration
    :param waitTime: int > 1 [minutes]
                     The time the train waits on each station, up to. for example = 1 gives times between 0-60 seconds
                     according to assignment specification
    :param waitTimeEndIn: int, The time the train waits on the end stations.
    :param startHourIn: int, specify the departure hour for the first train
    :param startMinuteIn: int, specify the departure minute for the first train
    :param endHourIn: int, specify the departure hour for the last train from the last station
    :param endMinuteIn: int, specify the departure minute for the last train from the last station
    :param trainAm: int >= 0 The amount of trains that travels the line on weekdays
    :param trainAmWkd: int >= 0 The amount of trains that travels the line on weekdays
    :return: stations: a list of station objects
    """

    verifyValues(fileStations, train, waitTime, waitTimeEndIn, startHourIn, startMinuteIn, endHourIn, endMinuteIn,
                 trainAm, trainAmWkd)

    waitTimeEnd = datetime.timedelta(minutes=waitTimeEndIn)
    startTime = datetime.timedelta(hours=startHourIn, minutes=startMinuteIn)
    endTime = datetime.timedelta(hours=endHourIn, minutes=endMinuteIn)
    stations = []

    nr = -1
    # Cal
    for i in fileStations:
        nr += 1
        stations.append(Station(i[0], i[1]))
        if len(stations) > 1:
            stations[nr].distFromLast = stations[nr].distFromStart - stations[nr - 1].distFromStart

    # Sets travel times between the stations in the station objects, rounds according to assignment specification.
    for i in range(1, len(stations)):
        time = train.calTravelTime(stations[i].distFromLast)
        stations[i].travelTime = datetime.timedelta(minutes=(time // 60) + waitTime)

    # Calculating the travel time for the train to all the stations.
    for i in range(1, len(stations)):
        stations[i].timeFromStart = stations[i-1].timeFromStart + stations[i].travelTime

    stations[len(stations) - 1].timeFromEnd = stations[len(stations) - 1].timeFromStart + waitTimeEnd

    for i in reversed(range(0, len(stations)-1)):
        stations[i].timeFromEnd = stations[i+1].timeFromEnd + stations[i+1].travelTime

    listWeekday = makeTable(startTime, endTime, trainAm, stations[0].timeFromEnd, waitTimeEnd)
    listWeekend = makeTable(startTime, endTime, trainAmWkd, stations[0].timeFromEnd, waitTimeEnd)

    # Setting departure times from the travel times and given start time.
    for station in stations:
        depFromStart, depFromEnd = setDepartureTimes(listWeekday, station)
        depFromStartWkd, depFromEndWkd = setDepartureTimes(listWeekend, station)

        # You can not travel from a end station towards the same end station
        if station != stations[0]:
            station.departuresFromEnd += depFromEnd
            station.departuresFromEndWkd += depFromEndWkd
        if station != stations[len(stations)-1]:
            station.departuresFromStart += depFromStart
            station.departuresFromStartWkd += depFromStartWkd

    return stations
