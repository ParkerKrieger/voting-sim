import unittest
import numpy as np
from Plurality import Plurality
from Simulation import Simulation


class MyTestCase(unittest.TestCase):
    def test_winner(self):
        sim = Simulation(4, 2)
        sim.accuracyScores = np.array([1, 0, 0, 0])
        sim.confidenceScores = np.array([[1, 0, 0, 0],
                                         [1, 0, 0, 0],
                                         [1, 0, 0, 0],
                                         [1, 0, 0, 0]])
        sim.rankings = np.array([[1, 2],
                                 [2, 1],
                                 [2, 1],
                                 [2, 1]])
        plurality = Plurality.from_sim(sim)
        result = plurality.calculate_winner()
        assert result == 0


if __name__ == '__main__':
    unittest.main()
