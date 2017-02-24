from __future__ import print_function

#!/usr/bin/env python
__author__ = 'Thomas Rueckstiess, ruecksti@in.tum.de'

from karr_environment import KarrEnvironment
from karr_task import KarrTask
from pybrain.rl.agents import LearningAgent
from pybrain.rl.experiments import ContinuousExperiment
from pybrain.rl.learners.valuebased import NFQ, ActionValueNetwork
from pybrain.rl.explorers import BoltzmannExplorer

from numpy import array, arange, meshgrid, pi, zeros, mean
from matplotlib import pyplot as plt
from pybrain.tools.customxml import NetworkWriter, NetworkReader
import RPi.GPIO as GPIO

# switch this to True if you want to see the cart balancing the pole (slower)
render = False

plt.ion()

env = KarrEnvironment()

module = ActionValueNetwork(3, 7)
try:
  module.network = NetworkReader.readFrom("savedNetwork.xml")
except:
  print("No network file")

task = KarrTask(env)
learner = NFQ()
learner.explorer.epsilon = 0.4

agent = LearningAgent(module, learner)

testagent = LearningAgent(module, None)
experiment = ContinuousExperiment(task, agent)

def plotPerformance(values, fig):
    plt.figure(fig.number)
    plt.clf()
    plt.plot(values, 'o-')
    plt.gcf().canvas.draw()
    # Without the next line, the pyplot plot won't actually show up.
    plt.pause(0.001)

performance = []

#if not render:
pf_fig = plt.figure()


try:
    print("Press ctrt + c to stop and exit")
    experiment.doInteractions(10)

    while(True):
        # one learning step after one episode of world-interaction
        experiment.doInteractionsAndLearn(10)
        #r = mean([sum(x) for x in experiment.doInteractions(10)])
        #agent.learn(1)

        # test performance (these real-world experiences are not used for training)
        #if render:
        #    env.delay = True
        #experiment.agent = testagent
        #r = mean([sum(x) for x in experiment.doInteractions(5)])
        #env.delay = False
        #testagent.reset()
        #experiment.agent = agent

        r = agent.lastreward
        performance.append(r)
        #if not render:
        plotPerformance(performance, pf_fig)

        NetworkWriter.writeToFile(agent.module.network, "savedNetwork.xml")
        print("reward avg", r)
        print("explorer epsilon", learner.explorer.epsilon)
        print("num episodes", agent.history.getNumSequences())
        print("update step", len(performance))

except KeyboardInterrupt:
    print("Shutting down")
    GPIO.cleanup()
