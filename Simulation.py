import numpy as np
import random

class Simulation(object):
    """
    Simulation Interface

    The simulation class contains a list of accuracy scores, confidence scores, and rankings representing the agents
    involved in the simulation.
    """

    def __init__(self, voters=20, candidates=4, accMean=0.5, accDev=0.1, confMean=0.5, confDev=0.2):
        self.voters = voters
        self.candidates = candidates
        self.accuracyScores = np.random.normal(accMean, accDev, voters)
        self.confidenceScores = np.random.normal(confMean, confDev, (voters, voters))
        self.rankings = self.createRankings()

    def createRankings(self):
        rankings = []
        for i in range(self.voters):
            rankList = [num for num in range(1, self.candidates + 1)]

            if random.random() > self.accuracyScores[i]:
                random.shuffle(rankList)

            rankings.append(np.array(rankList))

        return np.array(rankings)

    def adjustConfidence(self, adjust=0.05):
        for i in range(self.voters):
            if self.rankings[i][0] == 1:
                for j in range(self.voters):
                    self.confidenceScores[j][i] = min((self.confidenceScores[j][i]*(1+adjust)), 1)
            else:
                for j in range(self.voters):
                    self.confidenceScores[j][i] = max((self.confidenceScores[j][i]*(1-adjust)), 0)
