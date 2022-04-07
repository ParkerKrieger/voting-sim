import numpy as np
import random

class Simulation(object):
    """
    Simulation Interface

    The simulation class contains a list of accuracy scores, confidence scores, and rankings representing the agents
    involved in the simulation.
    """

    def __init__(self, voters=20, candidates=4):
        self.voters = voters
        self.candidates = candidates
        self.accuracyScores = np.random.normal(0.5, 0.1, voters)
        self.confidenceScores = np.random.normal(0.5, 0.1, (voters, voters))
        self.rankings = self.__createRankings()

    def __createRankings(self):
        rankings = []
        for i in range(self.voters):
            rankList = [num for num in range(1, self.candidates+1)]
            random.shuffle(rankList)
            rankings.append(np.array(rankList))

        return np.array(rankings)
