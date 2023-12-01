import unittest

from novi.client.activations import activation_util
from novi.core.models import ActivationModel, FlagModel
import logging.config
from novi.client import flag
logging.config.fileConfig("logging.conf")


class FlagClientTest(unittest.TestCase):
    def test_AND_allTrue(self):
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
        fl = FlagModel(id=1, name="test feature flag", activations = [dta, wr], status=True)
        self.assertEqual(True, flag.evaluate_flag(fl, context).status)

    def test_AND_FalseTrue(self):
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

        fl = FlagModel(id=1, name="test feature flag", activations = [dta, wr], status=True)
        self.assertEqual(flag.evaluate_flag(fl, context).status, False)

    def test_OR_allTrue(self):
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
        self.assertEqual(True, activation_util.or_all_activations([dta, wr], context))

    def test_OR_FalseTrue(self):
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

        self.assertEqual(True, activation_util.or_all_activations([dta, wr], context))

    def test_FlagFalse(self):
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
        fl = FlagModel(id=1, name="test feature flag", activations = [dta, wr], status=False)
        self.assertEqual(False, flag.evaluate_flag(fl, context).status)


if __name__ == '__main__':
    unittest.main()
