import logging
import unittest

from novi_activations.standard.weighted_random_activation import WeightedRandomActivation

logger = logging.getLogger(__name__)


class WeightedRandomTestCase(unittest.TestCase):

    def test_evaluate_A(self):
        # Given the 100, 0, 0 split always evaluates for A for any seed
        wr = WeightedRandomActivation('{ "splits":[100, 0, 0], "variations":["A", "B", "C"]}')
        self.assertEqual(True, wr.evaluate({'seed': 90, 'variant': 'A'}))
        self.assertEqual(False, wr.evaluate({'seed': 90, 'variant': 'B'}))
        self.assertEqual(False, wr.evaluate({'seed': 90, 'variant': 'C'}))

    def test_evaluate_B(self):
        # Given the 0, 100, 0 split always evaluates for B for any seed
        wr = WeightedRandomActivation('{ "splits":[0, 100, 0], "variations":["A", "B", "C"]}')
        self.assertEqual(False, wr.evaluate({'seed': 90, 'variant': 'A'}))
        self.assertEqual(True, wr.evaluate({'seed': 90, 'variant': 'B'}))
        self.assertEqual(False, wr.evaluate({'seed': 90, 'variant': 'C'}))


if __name__ == '__main__':
    unittest.main()
