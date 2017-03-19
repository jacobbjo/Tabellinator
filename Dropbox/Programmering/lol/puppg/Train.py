__author__ = 'Jacob'
__copyright__ = "May 2015"
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math
class Train(object):
    """
    Object class that contains attributes for train performance and a method to calculate the time it takes to travel a
    distance
    """

    def __init__(self, acceleration, retardation, maxSpeed):
        """
        Creates an instance of the class to contain attributes for train performance.

        :param acceleration: int, positive, the trains acceleration in m/s^2
        :param retardation: int, positive, the trains retardation in m/s^2
        :param maxSpeed: int, positive, the trains max speed in m/s
        attributes: acceleration: int, positive, the trains acceleration in m/s^2
                    retardation: int, positive, the trains retardation in m/s^2
                    maxSpeed: int, positive, the trains max speed in m/s
                    toMax: float, positive, the distance it takes for the train to reach max speed
                    toStop: float, positive, the distance it takes for the train to reach absolute stop from max speed
        """
        self.acceleration = float(acceleration)
        self.retardation = float(retardation)
        self.maxSpeed = float(maxSpeed)
        self.toMax = self.calDist(acceleration)
        self.toStop = self.calDist(retardation)

    def __str__(self):
        """
        A method to turn the attributes for the object into a string, designed for primary use in a console printout

        :return: a string with multiple lines
        """
        return"************************************" +\
              "\nAcceleration: " + str(self.acceleration) + " m/s^2" + \
              "\nRetardation: " + str(self.retardation) + " m/s^2" + \
              "\nMax speed: " + str(self.maxSpeed) + " m/s" + \
              "\nDistance to max speed: " + str(self.toMax) + " m" + \
              "\nDistance to stop: " + str(self.toStop) + " m" + \
              "\n************************************"

    def calDist(self, accRet):
        """
        Calculates the distance the train need to accelerate to max speed or break to a complete stop.
        raises ValueError if negative acceleration of retardation is put in.

        :param accRet: int [m/s^2] The value of the acceleration or retardation
        :return: dist: float [m] The distance to max speed or complete stop
        """
        if accRet <= 0:
            raise ValueError
        dist = (self.maxSpeed**2)/(2*accRet)
        return dist

    def calTravelTime(self, distance):
        """
        Calculates the time it takes for the train to travel a certain distance

        :param distance: float [m] the distance to be traveled by the train
        :return: time: float [s], the time it takes to travel the distance
        """
        if distance <= self.toMax:
            time = math.sqrt(2 * distance * ((1 / self.acceleration) + (1 / self.retardation)))
        else:
            time = self.maxSpeed * ((1 / self.acceleration) + (1 / self.retardation)) + (distance - self.toMax - self.toStop)/self.maxSpeed
        return time