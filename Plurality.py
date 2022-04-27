from Simulation import Simulation
import numpy as np


class Plurality(object):
    """
    Contains all the logic needed to simulate a plurality election using liquid democracy.
    """

    def __init__(self, voters=20, candidates=4, iterations=50, accMean=0.5, accDev=0.1, confMean=0.5, confDev=0.2):
        self.simulation = Simulation(voters, candidates, accMean, accDev, confMean, confDev)
        self.votes = None
        self.candidateVotes = None
        self.iterations = iterations

    @classmethod
    def fromSim(cls, simulation):
        plurality = cls(simulation.voters, simulation.candidates)
        plurality.simulation = simulation
        return plurality

    def calculateWinner(self):
        self.votes = self.simulation.calculateVotes()
        self.candidateVotes = np.zeros(self.simulation.candidates)

        for i in range(self.simulation.voters):
            numVotes = self.votes[i]
            if numVotes != 0:
                self.candidateVotes[self.simulation.rankings[i].argmin()] += self.votes[i]

        return self.candidateVotes.argmax()

    def runSim(self, adjust=0.05):
        for i in range(self.iterations - 1):
            self.calculateWinner()
            self.simulation.adjustConfidence(adjust)
            self.simulation.createRankings()

        return self.calculateWinner()

if __name__ == '__main__':
    data = [0] * 4
    for i in range(50):
        plurality = Plurality(voters=100,
                              candidates=4,
                              iterations=5,
                              accMean=0.25,
                              accDev=0.1,
                              confMean=0.5,
                              confDev=0.2)
        winner = plurality.runSim(0.05)
        data[winner] += 1
    print(winner)
    print(data)

    data = [0] * 4
    for i in range(50):
        plurality = Plurality(voters=250,
                              candidates=4,
                              iterations=5,
                              accMean=0.25,
                              accDev=0.1,
                              confMean=0.5,
                              confDev=0.2)
        winner = plurality.runSim(0.05)
        data[winner] += 1
    print(winner)
    print(data)

    data = [0] * 4
    for i in range(50):
        plurality = Plurality(voters=500,
                              candidates=4,
                              iterations=5,
                              accMean=0.25,
                              accDev=0.1,
                              confMean=0.5,
                              confDev=0.2)
        winner = plurality.runSim(0.05)
        data[winner] += 1
    print(winner)
    print(data)
