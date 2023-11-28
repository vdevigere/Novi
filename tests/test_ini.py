import logging
import unittest
import okapi.core
import okapi_activations.activation1 as activation1
import okapi_activations.activation2 as activation2
import okapi_activations.sub_package.activation3 as activation3
import okapi_activations.standard.weighted_random_activation as wra
import okapi_activations.standard.date_time_activation as dta

logger = logging.getLogger(__name__)


class OkapiActivationDiscoveryTest(unittest.TestCase):
    def test_discovery(self):
        expectedDict = {
            "okapi_activations.activation1.Activation1": activation1.Activation1,
            "okapi_activations.activation2.Activation2": activation2.Activation2,
            "okapi_activations.standard.weighted_random_activation.WeightedRandomActivation": wra.WeightedRandomActivation,
            'okapi_activations.standard.date_time_activation.DateTimeActivation': dta.DateTimeActivation,
            "okapi_activations.sub_package.activation3.Activation3": activation3.Activation3
        }
        self.assertEqual(expectedDict, okapi.core.discovered_activations)


if __name__ == '__main__':
    unittest.main()
