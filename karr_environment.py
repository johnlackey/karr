__author__ = 'Tom Schaul, tom@idsia.ch'

from random import random, choice
from scipy import zeros

from pybrain.utilities import Named
from pybrain.rl.environments.environment import Environment

import numpy as np
import time
# TODO: mazes can have any number of dimensions?
import Car


class KarrEnvironment(Environment, Named):
    car = None
    # table of booleans
    # mazeTable = None

    # single goal
    # goal = None

    # current state
    # perseus = None

    # list of possible initial states
    # initPos = None

    # directions
    Forward = "w"
    Right = "e"
    Left = "q"
    Reverse = "x"
    Stop = "s"
    ReverseRight = "c"
    ReverseLeft = "z"

    allActions = [Forward, Right, Left, Reverse, Stop, ReverseRight, ReverseLeft]

    # stochasticity
    stochAction = 0.0
    stochObs = 0.

    def __init__(self, **args):
        self.setArgs(**args)
        self.car = Car.Car()

    def command(self, action):
        speed = 200
        print(action)
        if action == "q":
            self.car.forward(speed)
            self.car.left(speed)
            self.direction = 1
        elif action == "w":
            self.car.forward(speed)
            self.car.straight()
            self.direction = 1
        elif action == "e":
            self.car.forward(speed)
            self.car.right(speed)
            self.direction = 1
        elif action == "z":
            self.car.backward(speed)
            self.car.left(speed)
            self.direction = -1
        elif action == "x":
            self.car.backward(speed)
            self.car.straight()
            self.direction = -1
        elif action == "c":
            self.car.backward(speed)
            self.car.right(speed)
            self.direction = -1
        elif action == "a":
            self.car.stop()
            self.direction = 0
        elif action == "d":
            self.car.stop()
            self.direction = 0
        elif action == "s":
            self.car.stop()
            self.direction = 0
        time.sleep(1)
        self.car.stop()

    def performAction(self, action):
        # action = 1
        action = np.int_(action[0])
        if self.stochAction > 0:
            if random() < self.stochAction:
                action = choice(list(range(len(self.allActions))))
        print("Action: ", action)
        tmp = self.command(self.allActions[action])

    def getDirection(self):
        return self.direction

    def getDistance(self, sensor=0):
        return self.car.distance(sensor)

    def getSensors(self):
        sensors = [self.getDistance(0), self.getDistance(1), self.getDistance(2)]
        if min(sensors) < 10:
            # self.command("x")
            self.command("c")
        return sensors
