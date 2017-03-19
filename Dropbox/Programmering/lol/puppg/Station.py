__author__ = 'Jacob'
__copyright__ = "May 2015"
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
class Station(object):
    """
    Object class that contains attributes for station location and departures
    """
    def __init__(self, name, distFromStart):
        """
        Creates an instance of the class to contain attributes for station location and departures

        :param name: string, name of the station
        :param distFromStart: float [km], the distance from the start station
        attributes: name: string, name of station
                    distFromStart: float [m] distance on the rail from the start station
                    distFromLast: float [m] distance on the rail from the last station
                    travelTime: datetime.timedelta object, time it takes to travel to the station from the previous
                    timeFromStart: datetime.timedelta object, time it takes to travel to the station from the start
                    timeFromEnd: datetime.timedelta object, time it takes to travel to the station from last station
                    departuresFromStart: list, containing datetime.timedelta objects with departures from start station
                    departuresFromEnd: list, containing datetime.timedelta objects with departures from last station
                    departuresFromStartWkd: list, containing datetime.timedelta objects with departures from start
                                            station on weekends
                    departuresFromEndWkd: list, containing datetime.timedelta objects with departures from last
                                            station on weekends

        """
        self.name = str(name)
        self.distFromStart = float(distFromStart) * 1000
        self.distFromLast = 0
        self.travelTime = datetime.timedelta(seconds=0)
        self.timeFromStart = datetime.timedelta(seconds=0)
        self.timeFromEnd = datetime.timedelta(seconds=0)
        self.departuresFromStart = []
        self.departuresFromEnd = []
        self.departuresFromStartWkd = []
        self.departuresFromEndWkd = []


    def __str__(self):
        """
        A method to turn the attributes for the object into a string, designed for primary use in a console printout

        :return: a string with multiple lines
        """
        return"************************************" +\
              "\nStationsnamn: " + self.name + \
              "\nAvstånd från start: " + str(self.distFromStart) + \
              "\nAvstånd från föregående: " + str(self.distFromLast) + \
              "\nRestid: " + str(self.travelTime) + \
              "\nTid från start: " + str(self.timeFromStart) + \
              "\nTid från slut: " + str(self.timeFromEnd) + \
              "\n************************************"


    def departuresStr(self, list):
        """
        Converts a list of datetime.timedelta objects to a sting with multiple lines for presentation

        :param list: a list of datetime.timedelta
        :return: string: a sting with multiple lines with a departure time on each line
        """
        string = ""
        for timeObj in list:
            hours, rem = divmod(timeObj.seconds, 3600)
            minutes, seconds = divmod(rem, 60)
            if hours < 10:
                hoursStr = "0" + str(hours)
            else:
                hoursStr = str(hours)

            if minutes < 10:
                minutesStr = "0" + str(minutes)
            else:
                minutesStr = str(minutes)

            string += (hoursStr + ":" + minutesStr + "\n")
        return string

    def departuresFromStartStr(self):
        """
        calls departuresStr to get a string of departure times from the start station
        :return: a string of departure times
        """
        return self.departuresStr(self.departuresFromStart)

    def departuresFromEndStr(self):
        """
        calls departuresStr to get a string of departure times from the end station
        :return: a string of departure times
        """
        return self.departuresStr(self.departuresFromEnd)

    def departuresFromStartWkdStr(self):
        """
        calls departuresStr to get a string of departure times from the start station on weekends
        :return: a string of departure times
        """
        return self.departuresStr(self.departuresFromStartWkd)

    def departuresFromEndWkdStr(self):
        """
        calls departuresStr to get a string of departure times from the end station on weekends
        :return: a string of departure times
        """
        return self.departuresStr(self.departuresFromEndWkd)
