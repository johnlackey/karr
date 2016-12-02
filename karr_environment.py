__author__ = 'Tom Schaul, tom@idsia.ch'

from random import random, choice
from scipy import zeros

from pybrain.utilities import Named
from pybrain.rl.environments.environment import Environment

# TODO: mazes can have any number of dimensions?
import Car

class KarrEnvironment(Environment, Named):

    car = None
    # table of booleans
    #mazeTable = None

    # single goal
    #goal = None

    # current state
    #perseus = None

    # list of possible initial states
    #initPos = None

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
    stochAction = 0.
    stochObs = 0.

    def __init__(self, **args):
        self.setArgs(**args)
        self.car = Car.Car()

    def command(self, action):
        speed = 255
        if action == "q":
            self.car.forward(speed)
            self.car.left(speed)
        elif action == "w":
            self.car.forward(speed)
            self.car.straight()
        elif action == "e":
            self.car.forward(speed)
            self.car.right(speed)
        elif action == "z":
            self.car.backward(speed)
            self.car.left(speed)
        elif action == "x":
            self.car.backward(speed)
            self.car.straight()
        elif action == "c":
            self.car.backward(speed)
            self.car.right(speed)
        elif action == "a":
            self.car.stop()
        elif action == "d":
            self.car.stop()
        elif action == "s":
            self.car.stop()

    def performAction(self, action):
        if self.stochAction > 0:
            if random() < self.stochAction:
                action = choice(list(range(len(self.allActions))))
        tmp = self.command(self.allActions[action])

    def getDistance(self):
        return 1

    def getSensors(self):
        return self.getDistance()



