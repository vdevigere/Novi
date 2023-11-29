import unittest

from novi.client.activations.composite_and_activation import CompositeAndActivation
from novi.core.models import ActivationModel
import logging.config

logging.config.fileConfig("logging.conf")


class CompositeActivationTestCase(unittest.TestCase):
    def test_allTrue(self):
        dta = ActivationModel(id=1, name="date-time",
                              class_name="novi.client.activations.date_time_activation.DateTimeActivation",
                              config='''{
                "startDateTime":"11/26/2023 12:00 AM",
                "endDateTime":"11/28/2023 12:00 AM",
                "format": "%m/%d/%Y %I:%M %p"
                }''')
        wr = ActivationModel(id=1, name="date-time",
                             class_name="novi.client.activations.weighted_random_activation.WeightedRandomActivation",
                             config='{ "splits":[100, 0, 0], "variations":["A", "B", "C"]}')

        context = {
            'currentDateTime': '11/27/2023 12:00 AM',
            'seed': 90,
            'variant': 'A'
        }

        cpa = CompositeAndActivation([dta, wr])
        self.assertEqual(cpa.evaluate(context), True)

    def test_FalseTrue(self):
        dta = ActivationModel(id=1, name="date-time",
                              class_name="novi.client.activations.date_time_activation.DateTimeActivation",
                              config='''{
                "startDateTime":"11/26/2023 12:00 AM",
                "endDateTime":"11/28/2023 12:00 AM",
                "format": "%m/%d/%Y %I:%M %p"
                }''')
        wr = ActivationModel(id=1, name="date-time",
                             class_name="novi.client.activations.weighted_random_activation.WeightedRandomActivation",
                             config='{ "splits":[100, 0, 0], "variations":["A", "B", "C"]}')

        context = {
            'currentDateTime': '11/28/2023 12:00 AM',
            'seed': 90,
            'variant': 'A'
        }

        cpa = CompositeAndActivation([dta, wr])
        self.assertEqual(cpa.evaluate(context), False)


if __name__ == '__main__':
    unittest.main()
