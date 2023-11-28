import unittest

from novi_activations.standard.date_time_activation import DateTimeActivation


class DateTimeActivationTestCase(unittest.TestCase):
    def test_inbetween(self):
        dta = DateTimeActivation('''{
        "startDateTime":"11/26/2023 12:00 AM",
        "endDateTime":"11/28/2023 12:00 AM",
        "format": "%m/%d/%Y %I:%M %p"
        }''')
        context = {
            'currentDateTime': '11/27/2023 12:00 AM'
        }
        res = dta.evaluate(context=context)
        self.assertEqual(True, res)

    def test_after(self):
        dta = DateTimeActivation('''{
        "startDateTime":"11/26/2023 12:00 AM",
        "endDateTime":"11/28/2023 12:00 AM",
        "format": "%m/%d/%Y %I:%M %p"
        }''')
        context = {
            'currentDateTime': '11/29/2023 12:00 AM'
        }
        res = dta.evaluate(context=context)
        self.assertEqual(False, res)

    def test_before(self):
        dta = DateTimeActivation('''{
        "startDateTime":"11/26/2023 12:00 AM",
        "endDateTime":"11/28/2023 12:00 AM",
        "format": "%m/%d/%Y %I:%M %p"
        }''')
        context = {
            'currentDateTime': '11/25/2023 12:00 AM'
        }
        res = dta.evaluate(context=context)
        self.assertEqual(False, res)

    def test_equal_start(self):
        dta = DateTimeActivation('''{
        "startDateTime":"11/26/2023 12:00 AM",
        "endDateTime":"11/28/2023 12:00 AM",
        "format": "%m/%d/%Y %I:%M %p"
        }''')
        context = {
            'currentDateTime': '11/26/2023 12:00 AM'
        }
        res = dta.evaluate(context=context)
        self.assertEqual(True, res)

    def test_equal_end(self):
        dta = DateTimeActivation('''{
        "startDateTime":"11/26/2023 12:00 AM",
        "endDateTime":"11/28/2023 12:00 AM",
        "format": "%m/%d/%Y %I:%M %p"
        }''')
        context = {
            'currentDateTime': '11/28/2023 12:00 AM'
        }
        res = dta.evaluate(context=context)
        self.assertEqual(False, res)


if __name__ == '__main__':
    unittest.main()
