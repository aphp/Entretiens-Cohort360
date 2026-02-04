from unittest import TestCase
from datetime import date
from medical.management.commands.seed_demo import random_interval_between


class RandomIntervalHelperTestCase(TestCase):
    def test_smoke(self):
        # arrange
        not_before = date(year=2020, month=4, day=6)
        not_after = date(year=2030, month=1, day=20)

        # act
        actual_from, actual_to = random_interval_between(not_before, not_after)

        # assert
        self.assertGreater(actual_from, not_before)
        self.assertGreater(actual_to, actual_from)
        self.assertGreater(not_after, actual_to)

    # TODO other tests, such as testing boundaries or unordered parameters
