from Simulation import Simulation
import numpy as np


class Veto(object):
    """
    Contains all the logic needed to simulate a veto election using liquid democracy.
    """

    def __init__(self, voters=20, candidates=4, iterations=50, accMean=0.5, accDev=0.1, confMean=0.5, confDev=0.2):
        self.simulation = Simulation(voters, candidates, accMean, accDev, confMean, confDev)
        self.candidateVotes = None
        self.iterations = iterations

    @classmethod
    def fromSim(cls, simulation):
        veto = cls(simulation.voters, simulation.candidates)
        veto.simulation = simulation
        return veto

    def calculateWinner(self):
        rankings = self.simulation.rankings.copy()
        votes = self.simulation.calculateVotes()
        self.candidateVotes = np.zeros(self.simulation.candidates)
        for _ in range(self.simulation.candidates - 1):
            self.candidateVotes = np.zeros(self.simulation.candidates)

            for i in range(len(votes)):
                numVotes = votes[i]
                if numVotes != 0:
                    lastPlace = rankings[i].argmax()
                    self.candidateVotes[lastPlace] += numVotes

            loser = self.candidateVotes.argmax()

            for rank in rankings:
                rank[loser] = 0

        return rankings[0].argmax()



    def runSim(self, adjust=0.05):
        for i in range(self.iterations - 1):
            self.calculateWinner()
            self.simulation.adjustConfidence(adjust)
            self.simulation.createRankings()

        return self.calculateWinner()

if __name__ == '__main__':
    data = [0] * 4
    for i in range(50):
        veto = Veto(voters=100,
                              candidates=4,
                              iterations=5,
                              accMean=0.25,
                              accDev=0.1,
                              confMean=0.5,
                              confDev=0.2)
        winner = veto.runSim(0.05)
        data[winner] += 1
    print(winner)
    print(data)

    data = [0] * 4
    for i in range(50):
        veto = Veto(voters=500,
                              candidates=4,
                              iterations=5,
                              accMean=0.25,
                              accDev=0.1,
                              confMean=0.5,
                              confDev=0.2)
        winner = veto.runSim(0.05)
        data[winner] += 1
    print(winner)
    print(data)

    data = [0] * 4
    for i in range(50):
        veto = Veto(voters=1000,
                              candidates=4,
                              iterations=5,
                              accMean=0.25,
                              accDev=0.1,
                              confMean=0.5,
                              confDev=0.2)
        winner = veto.runSim(0.05)
        data[winner] += 1
    print(winner)
    print(data)
