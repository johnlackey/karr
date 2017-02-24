__author__ = 'Tom Schaul, tom@idsia.ch'

from scipy import array

from pybrain.rl.environments.mazes import Maze
from pybrain.rl.environments.episodictask import EpisodicTask


class KarrTaskEpisodic(EpisodicTask):
    """ a task corresponding to a karr environment """

    bangPenalty = 0
    defaultPenalty = 0
    finalReward = 1

    topology = None
    goal = None
    initPos = None
    mazeclass = Maze

    stochObs = 0
    stochAction = 0

    @property
    def noisy(self):
        return self.stochObs > 0

    def __init__(self, env):
        Task.__init__(self, env)
        self.minReward = min(self.bangPenalty, self.defaultPenalty)
        self.finished = False

    def getReward(self):
        #if 100 == 0:
        #    return self.finalReward
        #elif self.env.bang:
        #    return self.bangPenalty
        #else:
        #return self.defaultPenalty
        minDistance = min(self.env.getSensors())
        if minDistance < 10:
            reward = -10
            self.finished = True
        elif minDistance < 50:
            reward =  -2
        else:
            reward = 1 * self.env.getDirection()
        print "Reward: %d" % reward
        return reward

    #def reset(self):
    #    print("KarrTask::reset")

    def isFinished(self):
        return self.finished or self.env.perseus == self.env.goal or POMDPTask.isFinished(self)

    def __str__(self):
        return str(self.env)


class TrivialKarr(KarrTask):
    """
    #####
    #. *#
    #####
    """
    discount = 0.8
    initPos = [(1, 1)]
    topology = array([[1] * 5,
                      [1, 0, 0, 0, 1],
                      [1] * 5, ])
    goal = (1, 3)

