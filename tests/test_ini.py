import logging
import unittest

import novi.core
import novi_activations.activation1 as activation1
import novi_activations.activation2 as activation2
import novi.client.activations.date_time_activation as dta
import novi.client.activations.weighted_random_activation as wra
import novi_activations.sub_package.activation3 as activation3
import novi.client.activations.and_activation as aa
import novi.client.activations.or_activation as oa
logger = logging.getLogger(__name__)


class noviActivationDiscoveryTest(unittest.TestCase):
    def test_discovery(self):
        expectedDict = {
            'novi.client.activations.and_activation.AndActivation': aa.AndActivation,
            'novi.client.activations.or_activation.OrActivation': oa.OrActivation,
            "novi_activations.activation1.Activation1": activation1.Activation1,
            "novi_activations.activation2.Activation2": activation2.Activation2,
            "novi.client.activations.weighted_random_activation.WeightedRandomActivation": wra.WeightedRandomActivation,
            'novi.client.activations.date_time_activation.DateTimeActivation': dta.DateTimeActivation,
            "novi_activations.sub_package.activation3.Activation3": activation3.Activation3
        }
        self.assertEqual(expectedDict, novi.core.discovered_activations)


if __name__ == '__main__':
    unittest.main()
