from Ranked import Ranked
from Plurality import Plurality
from Veto import Veto
import matplotlib.pyplot as plt
import numpy as np


if __name__ == '__main__':
    voters = 20
    candidates = 4
    iterations = 1
    accMean = 0.5
    accDev = 0.1
    confMean = 0.5
    confDev = 0.01

    liqPluralityPlt = []
    pluralityPlt = []
    liqRankedPlt = []
    rankedPlt = []
    liqVetoPlt = []
    vetoPlt = []
    y = []

    for iteration in range(1,6):
        pluralityLiquidData = [0] * candidates
        pluralityData = [0] * candidates
        rankedLiquidData = [0] * candidates
        rankedData = [0] * candidates
        vetoLiquidData = [0] * candidates
        vetoData = [0] * candidates

        for i in range(100):
            liqPlurality = Plurality(voters=voters,
                                  candidates=candidates,
                                  iterations=iteration,
                                  accMean=accMean,
                                  accDev=accDev,
                                  confMean=confMean,
                                  confDev=confDev
                                  )
            winner = liqPlurality.runSim(0.1)
            pluralityLiquidData[winner] += 1


            plurality = Plurality(voters=voters,
                                  candidates=candidates,
                                  iterations=iterations,
                                  accMean=accMean,
                                  accDev=accDev,
                                  confMean=confMean,
                                  confDev=confDev,
                                  liquid=False
                                  )
            winner = plurality.runSim(0.1)
            pluralityData[winner] += 1

            liqRanked = Ranked(voters=voters,
                            candidates=candidates,
                            iterations=iteration,
                            accMean=accMean,
                            accDev=accDev,
                            confMean=confMean,
                            confDev=confDev
                            )
            winner = liqRanked.runSim(0.1)
            rankedLiquidData[winner] += 1

            ranked = Ranked(voters=voters,
                            candidates=candidates,
                            iterations=iterations,
                            accMean=accMean,
                            accDev=accDev,
                            confMean=confMean,
                            confDev=confDev,
                            liquid=False
                            )
            winner = ranked.runSim(0.1)
            rankedData[winner] += 1

            liqVeto = Veto(voters=voters,
                        candidates=candidates,
                        iterations=iteration,
                        accMean=accMean,
                        accDev=accDev,
                        confMean=confMean,
                        confDev=confDev
                        )
            winner = liqVeto.runSim(0.1)
            vetoLiquidData[winner] += 1

            veto = Veto(voters=voters,
                        candidates=candidates,
                        iterations=iterations,
                        accMean=accMean,
                        accDev=accDev,
                        confMean=confMean,
                        confDev=confDev,
                        liquid=False
                        )
            winner = veto.runSim(0.1)
            vetoData[winner] += 1
        # print(f"---------Iterations: {iteration}-------------")
        # print(f"Plurality Liquid Data: {pluralityLiquidData}")
        # print(f"Plurality Data: {pluralityData}")
        # print(f"Ranked Liquid Data: {rankedLiquidData}")
        # print(f"Ranked Data: {rankedData}")
        # print(f"Veto Liquid Data: {vetoLiquidData}")
        # print(f"Veto Data: {vetoData}")

        liqPluralityPlt.append(pluralityLiquidData[0])
        pluralityPlt.append(pluralityData[0])
        liqRankedPlt.append(rankedLiquidData[0])
        rankedPlt.append(rankedData[0])
        liqVetoPlt.append(vetoLiquidData[0])
        vetoPlt.append(vetoData[0])
        y.append(iteration)

    plt.plot(y, liqPluralityPlt, label = "Liquid Plurality")
    plt.plot(y, liqRankedPlt, label="Liquid Ranked")
    plt.plot(y, liqVetoPlt, label="Liquid Veto")
    plt.plot(y, pluralityPlt, label="Plurality")
    plt.plot(y, rankedPlt, label="Ranked")
    plt.plot(y, vetoPlt, label="Veto")
    plt.legend()
    plt.title("Low Confidence Mean")
    plt.xlabel("Iterations")
    plt.ylabel("# of correct votes")
    plt.savefig("Graphs/High ConfDev (iterations).png")

