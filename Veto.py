from Simulation import Simulation
import numpy as np


class Veto(object):
    """
    Contains all the logic needed to simulate a veto election using liquid democracy.
    """

    def __init__(self, voters=20, candidates=4, iterations=50, accMean=0.5, accDev=0.1, confMean=0.5, confDev=0.2):
        self.simulation = Simulation(voters, candidates, accMean, accDev, confMean, confDev)
        self.votes = None
        self.candidateVotes = None
        self.iterations = iterations

    @classmethod
    def fromSim(cls, simulation):
        veto = cls(simulation.voters, simulation.candidates)
        veto.simulation = simulation
        return veto

    def calculateWinner(self):
        rankings = self.simulation.rankings.copy()
        self.votes = self.calculateVotes()
        self.candidateVotes = np.zeros(self.simulation.candidates)
        for _ in range(self.simulation.candidates - 1):
            self.candidateVotes = np.zeros(self.simulation.candidates)

            for i in range(len(self.votes)):
                lastPlace = rankings[i].argmax()
                self.candidateVotes[lastPlace] += self.votes[i]

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

    def calculateVotes(self):
        votes = np.zeros(self.simulation.voters)
        voteGiven = True
        iterations = 0

        for i in range(self.simulation.voters):
            giveVote = self.simulation.confidenceScores[i].argmax()
            votes[giveVote] += 1

        while voteGiven and iterations < 10:
            voteGiven = False
            for i in range(self.simulation.voters):
                giveVote = self.simulation.confidenceScores[i].argmax()
                if giveVote != i:
                    voteGiven = True
                    votes[giveVote] += votes[i]
                    votes[i] = 0
            iterations += 1

        return votes

if __name__ == '__main__':
    data = [0] * 4
    for i in range(50):
        plurality = Veto(voters=100,
                              candidates=4,
                              iterations=25,
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
        plurality = Veto(voters=5000,
                              candidates=4,
                              iterations=25,
                              accMean=0.25,
                              accDev=0.1,
                              confMean=0.5,
                              confDev=0.2)
        winner = plurality.runSim(0.05)
        data[winner] += 1
    print(winner)
    print(data)

    data = [0] * 4
    for i in range(500):
        plurality = Veto(voters=25000,
                              candidates=4,
                              iterations=25,
                              accMean=0.25,
                              accDev=0.1,
                              confMean=0.5,
                              confDev=0.2)
        winner = plurality.runSim(0.05)
        data[winner] += 1
    print(winner)
    print(data)
