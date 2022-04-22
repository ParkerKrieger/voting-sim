from Simulation import Simulation
import numpy as np


class Plurality(object):
    """
    Contains all the logic needed to simulate a plurality election using liquid democracy.
    """

    def __init__(self, voters=20, candidates=4, iterations=50, accMean=0.5, accDev=0.1, confMean=0.5, confDev=0.2):
        self.simulation = Simulation(voters, candidates, accMean, accDev, confMean, confDev)
        self.votes = np.zeros(voters)
        self.candidateVotes = np.zeros(candidates)
        self.iterations = iterations

    @classmethod
    def from_sim(cls, simulation):
        plurality = cls(simulation.voters, simulation.candidates)
        plurality.simulation = simulation
        return plurality

    def calculate_winner(self):
        self.votes = np.zeros(self.simulation.voters)
        self.candidateVotes = np.zeros(self.simulation.candidates)
        for i in range(self.simulation.voters):
            giveVote = self.simulation.confidenceScores[i].argmax()
            self.votes[giveVote] += 1

        for i in range(self.simulation.voters):
            self.candidateVotes[self.simulation.rankings[i].argmin()] += self.votes[i]

        return self.candidateVotes.argmax()

    def runSim(self, adjust=0.05):
        for i in range(self.iterations - 1):
            self.calculate_winner()
            self.adjustConfidence(adjust)
            self.simulation.createRankings()

        return self.calculate_winner()

    def adjustConfidence(self, adjust=0.05):
        for i in range(self.simulation.voters):
            if self.simulation.rankings[i][0] == 1:
                for j in range(self.simulation.voters):
                    self.simulation.confidenceScores[j][i] = min((self.simulation.confidenceScores[j][i]*(1+adjust)), 1)
            else:
                for j in range(self.simulation.voters):
                    self.simulation.confidenceScores[j][i] = max((self.simulation.confidenceScores[j][i]*(1-adjust)), 0)

if __name__ == '__main__':
    data = [0] * 4
    for i in range(500):
        plurality = Plurality(voters=100,
                              candidates=4,
                              iterations=1,
                              accMean=0.25,
                              accDev=0.01,
                              confMean=0.5,
                              confDev=0.2)
        winner = plurality.runSim(0.1)
        data[winner] += 1
    print(winner)
    print(data)

    data = [0] * 4
    for i in range(500):
        plurality = Plurality(voters=100,
                              candidates=4,
                              iterations=10,
                              accMean=0.25,
                              accDev=0.01,
                              confMean=0.5,
                              confDev=0.2)
        winner = plurality.runSim(0.1)
        data[winner] += 1
    print(winner)
    print(data)

    data = [0] * 4
    for i in range(500):
        plurality = Plurality(voters=5,
                              candidates=4,
                              iterations=50,
                              accMean=0.25,
                              accDev=0.01,
                              confMean=0.5,
                              confDev=0.2)
        winner = plurality.runSim(0.1)
        data[winner] += 1
    print(winner)
    print(data)
