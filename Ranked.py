import math

from Simulation import Simulation
import numpy as np


class Ranked(object):
    """
    Contains all the logic needed to simulate a ranked election using liquid democracy.
    """

    def __init__(self, voters=20, candidates=4, iterations=50, accMean=0.5, accDev=0.1, confMean=0.5, confDev=0.2, liquid= True):
        self.simulation = Simulation(voters, candidates, accMean, accDev, confMean, confDev)
        self.votes = np.zeros(voters)
        self.candidateVotes = np.zeros(candidates)
        self.iterations = iterations
        self.liquid = liquid

    @classmethod
    def from_sim(cls, simulation):
        ranked = cls(simulation.voters, simulation.candidates)
        ranked.simulation = simulation
        return ranked

    def calculateWinner(self):
        eliminated = []
        if self.liquid:
            numVotes = self.simulation.calculateVotes()
        else:
            numVotes = [1] * self.simulation.voters
        # count first place rankings
        for i in range(self.simulation.candidates - 1):
            votes = [0 for i in range(self.simulation.candidates)]
            for elim in eliminated:
                votes[elim - 1] = math.inf
            for j in range(len(self.simulation.rankings)):
                total = numVotes[j]
                if total > 0:
                    ans = self.simulation.rankings[j][0]
                    if ans not in eliminated:
                        votes[ans - 1] += total

            # check for ties/find the winner
            last = []
            minVotes = min(votes)
            for x in range(len(votes)):
                if votes[x] == minVotes:
                    last.append(x + 1)

            # if there's a tie, find the loser, else add the loser to the list
            if len(last) > 1:
                eliminated.append(self.tieBreaker(last, self.simulation.rankings, self.simulation.candidates, self.simulation.candidates - 1))
            else:
                eliminated.append(last[0])

        winner = [elem for elem in self.simulation.rankings[0] if elem not in eliminated]
        winner = winner[0]
        return winner - 1

    def tieBreaker(self, last, order, candidates, lastIndex):
        if lastIndex < 1:
            return last[0]

        # find the last place people
        votes = [0 for i in range(candidates)]
        for j in range(len(order)):
            ans = order[j][lastIndex]
            if ans in last:
                votes[ans - 1] += 1

        # Check for a tie
        last = []
        maxVotes = max(votes)
        for x in range(len(votes)):
            if votes[x] == maxVotes:
                last.append(x + 1)

        # if there's a tie go through this again for the next to last index
        if len(last) > 1:
            return self.tieBreaker(last, order, candidates, lastIndex - 1)

        # Return the last place person
        return last[0]



    def runSim(self, adjust=0.05):
        for i in range(self.iterations - 1):
            self.calculateWinner()
            self.simulation.adjustConfidence(adjust)
            self.simulation.createRankings()

        return self.calculateWinner()

if __name__ == '__main__':
    print("-------Sim 1----------")
    data = [0] * 4
    for i in range(500):
        ranked = Ranked(voters=100,
                              candidates=4,
                              iterations=1,
                              accMean=0.25,
                              accDev=0.01,
                              confMean=0.5,
                              confDev=0.2)
        winner = ranked.runSim(0.1)
        data[winner] += 1
    print(winner)
    print(data)

    print("-------Sim 2----------")
    data = [0] * 4
    for i in range(500):
        ranked = Ranked(voters=100,
                              candidates=4,
                              iterations=3,
                              accMean=0.25,
                              accDev=0.01,
                              confMean=0.5,
                              confDev=0.2)
        winner = ranked.runSim(0.1)
        data[winner] += 1
    print(winner)
    print(data)

    print("-------Sim 3----------")
    data = [0] * 4
    for i in range(500):
        ranked = Ranked(voters=100,
                              candidates=4,
                              iterations=5,
                              accMean=0.25,
                              accDev=0.01,
                              confMean=0.5,
                              confDev=0.2)
        winner = ranked.runSim(0.1)
        data[winner] += 1
    print(winner)
    print(data)
