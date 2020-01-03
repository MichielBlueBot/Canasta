from collections import defaultdict
from unittest import TestCase

from base.utils.card_constants import POSSIBLE_SUIT
from base.utils.generators import ranks_list_generator, suit_series_generator, series_generator


class TestGamePhase(TestCase):

    def test_ranks_list_generator(self):
        min_length = 3
        max_length = 14
        count_by_length = defaultdict(int)
        for series in ranks_list_generator(min_length=min_length, max_length=max_length):
            count_by_length[len(series)] += 1
        for i in range(min_length, max_length + 1):
            self.assertEqual(14 - i + 1, count_by_length[i], msg="failed for {}".format(i))

    def test_suit_series_generator(self):
        min_length = 3
        max_length = 14
        for suit in POSSIBLE_SUIT:
            # All suits should generate an equal and correct amount of possible card series
            self.assertEqual(2655, len(list(suit_series_generator(suit=suit, min_length=min_length, max_length=max_length))))

    def test_series_generator(self):
        min_length = 3
        max_length = 14
        # This generator is simply the suit_series_generator looped over all series and thus should produce 4 times the resuts
        self.assertEqual(4*2655, len(list(series_generator(min_length=min_length, max_length=max_length))))
