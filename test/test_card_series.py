from unittest import TestCase

from base.card import Card, JOKER_RANK, JOKER_SUIT, POSSIBLE_SUIT
from base.cards.card_series import CardSeries
from base.enums.two_swap_direction import TwoSwapDirection


class TestCardSeries(TestCase):

    def test_add_front(self):
        card_set = CardSeries([Card(4, "hearts"), Card(5, "hearts"), Card(6, "hearts")])
        self.assertEqual(card_set.num_cards(), 3)
        new_card = Card(3, "hearts")
        card_set.add_front(new_card)
        self.assertEqual(card_set.num_cards(), 4)
        self.assertEqual(card_set.get_card(0), new_card)

    def test_add_back(self):
        card_set = CardSeries([Card(4, "hearts"), Card(5, "hearts"), Card(6, "hearts")])
        self.assertEqual(card_set.num_cards(), 3)
        new_card = Card(7, "hearts")
        card_set.add_back(new_card)
        self.assertEqual(card_set.num_cards(), 4)
        self.assertEqual(card_set.get_card(-1), new_card)

    def test_swap_joker(self):
        card_set_with_joker = CardSeries([Card(4, "hearts"), Card(JOKER_RANK, JOKER_SUIT), Card(6, "hearts")])
        swap_card = Card(5, "hearts")
        joker = card_set_with_joker.swap_joker(swap_card)
        self.assertTrue(joker.is_joker())
        self.assertEqual(card_set_with_joker.num_cards(), 3)
        self.assertFalse(card_set_with_joker.has_joker())

    def test_swap_two_front(self):
        card_set_with_two = CardSeries([Card(3, "hearts"), Card(2, "hearts"), Card(5, "hearts")])
        swap_card = Card(4, "hearts")
        card_set_with_two.swap_two(swap_card, direction=TwoSwapDirection.FRONT)
        self.assertEqual(card_set_with_two.num_cards(), 4)
        self.assertEqual(card_set_with_two.get_card(0), Card(2, "hearts"))

    def test_swap_two_front_edge_case(self):
        card_set_with_two = CardSeries([Card(2, "hearts"), Card(2, "hearts"), Card(4, "hearts")])
        swap_card = Card(3, "hearts")
        card_set_with_two.swap_two(swap_card, direction=TwoSwapDirection.FRONT)
        self.assertEqual(card_set_with_two.num_cards(), 4)
        self.assertEqual(card_set_with_two.get_card(0), Card(2, "hearts"))
        self.assertEqual(card_set_with_two.get_card(1), Card(2, "hearts"))
        self.assertEqual(card_set_with_two.get_card(2), Card(3, "hearts"))
        self.assertEqual(card_set_with_two.get_card(3), Card(4, "hearts"))

    def test_swap_two_back(self):
        card_set_with_two = CardSeries([Card(3, "hearts"), Card(2, "hearts"), Card(5, "hearts")])
        swap_card = Card(4, "hearts")
        card_set_with_two.swap_two(swap_card, direction=TwoSwapDirection.BACK)
        self.assertEqual(card_set_with_two.num_cards(), 4)
        self.assertEqual(card_set_with_two.get_card(-1), Card(2, "hearts"))

    def test_has_joker(self):
        card_set_no_joker = CardSeries([Card(4, "hearts"), Card(5, "hearts"), Card(6, "hearts")])
        self.assertFalse(card_set_no_joker.has_joker())
        card_set_with_joker = CardSeries([Card(4, "hearts"), Card(JOKER_RANK, JOKER_SUIT), Card(6, "hearts")])
        self.assertTrue(card_set_with_joker.has_joker())

    def test_has_two_joker(self):
        card_set_no_joker = CardSeries([Card(4, "hearts"), Card(5, "hearts"), Card(6, "hearts")])
        self.assertFalse(card_set_no_joker.has_two_joker())
        card_set_with_joker2 = CardSeries([Card(3, "hearts"), Card(2, "hearts"), Card(5, "hearts")])
        self.assertTrue(card_set_with_joker2.has_two_joker())

    def test_two_joker_proper_place(self):
        # This 2 is in the proper place so it's not a joker
        card_set = CardSeries([Card(2, "hearts"), Card(3, "hearts"), Card(4, "hearts")])
        self.assertFalse(card_set.has_two_joker())
        # This 2 is in the proper place so it's not a joker
        card_set = CardSeries([Card(1, "hearts"), Card(2, "hearts"), Card(3, "hearts")])
        self.assertFalse(card_set.has_two_joker())

    def test_validation(self):
        # VALID CARD SERIES
        for suit in POSSIBLE_SUIT:
            card_set = CardSeries([Card(2, suit), Card(3, suit), Card(4, suit)])
            self.assertTrue(card_set.is_valid())
            card_set = CardSeries([Card(11, suit), Card(12, suit), Card(13, suit)])
            self.assertTrue(card_set.is_valid())
            card_set = CardSeries([Card(1, suit), Card(2, suit), Card(3, suit)])
            self.assertTrue(card_set.is_valid())
            card_set = CardSeries([Card(3, suit), Card(2, suit), Card(5, suit)])
            self.assertTrue(card_set.is_valid())
            card_set = CardSeries([Card(2, suit), Card(2, suit), Card(4, suit)])
            self.assertTrue(card_set.is_valid())
            card_set = CardSeries([Card(4, suit), Card(JOKER_RANK, JOKER_SUIT), Card(6, suit)])
            self.assertTrue(card_set.is_valid())
            card_set = CardSeries([Card(JOKER_RANK, JOKER_SUIT), Card(6, suit), Card(7, suit)])
            self.assertTrue(card_set.is_valid())
            card_set = CardSeries([Card(4, suit), Card(5, suit), Card(JOKER_RANK, JOKER_SUIT)])
            self.assertTrue(card_set.is_valid())
        # INVALID CARD SERIES
        for suit in POSSIBLE_SUIT:
            card_set = CardSeries([Card(2, suit), Card(2, suit), Card(6, suit)])
            self.assertFalse(card_set.is_valid())
            card_set = CardSeries([Card(12, suit), Card(13, suit), Card(13, suit)])
            self.assertFalse(card_set.is_valid())
            card_set = CardSeries([Card(1, suit), Card(2, suit), Card(4, suit)])
            self.assertFalse(card_set.is_valid())
            card_set = CardSeries([Card(3, suit), Card(2, suit), Card(6, suit)])
            self.assertFalse(card_set.is_valid())
            card_set = CardSeries([Card(4, suit), Card(JOKER_RANK, JOKER_SUIT), Card(7, suit)])
            self.assertFalse(card_set.is_valid())
            card_set = CardSeries([Card(JOKER_RANK, JOKER_SUIT), Card(6, suit), Card(8, suit)])
            self.assertFalse(card_set.is_valid())
            card_set = CardSeries([Card(4, suit), Card(4, suit), Card(JOKER_RANK, JOKER_SUIT)])
            self.assertFalse(card_set.is_valid())
            card_set = CardSeries([Card(4, suit), Card(JOKER_RANK, JOKER_SUIT), Card(JOKER_RANK, JOKER_SUIT)])
            self.assertFalse(card_set.is_valid())

    def test_get_add_front_options(self):
        def check_options(card_series, correct_options):
            computed_options = card_series.get_add_front_options()
            self.assertEqual(computed_options, correct_options, msg="{}".format(card_series))

        for suit in POSSIBLE_SUIT:
            check_options(card_series=CardSeries([Card(2, suit), Card(3, suit), Card(4, suit)]),
                          correct_options=[Card(1, suit), Card(JOKER_RANK, JOKER_SUIT), Card(2, suit)])
            check_options(card_series=CardSeries([Card(11, suit), Card(12, suit), Card(13, suit)]),
                          correct_options=[Card(10, suit), Card(JOKER_RANK, JOKER_SUIT), Card(2, suit)])
            check_options(card_series=CardSeries([Card(1, suit), Card(2, suit), Card(3, suit)]),
                          correct_options=[])
            check_options(card_series=CardSeries([Card(3, suit), Card(2, suit), Card(5, suit)]),
                          correct_options=[Card(2, suit)])
            check_options(card_series=CardSeries([Card(2, suit), Card(2, suit), Card(4, suit)]),
                          correct_options=[Card(1, suit)])
            check_options(card_series=CardSeries([Card(2, suit), Card(JOKER_RANK, JOKER_SUIT), Card(4, suit)]),
                          correct_options=[Card(1, suit)])
            check_options(card_series=CardSeries([Card(4, suit), Card(JOKER_RANK, JOKER_SUIT), Card(6, suit)]),
                          correct_options=[Card(3, suit)])
            check_options(card_series=CardSeries([Card(JOKER_RANK, JOKER_SUIT), Card(6, suit), Card(7, suit)]),
                          correct_options=[Card(4, suit)])
            check_options(card_series=CardSeries([Card(4, suit), Card(5, suit), Card(JOKER_RANK, JOKER_SUIT)]),
                          correct_options=[Card(3, suit)])

    def test_get_add_back_options(self):
        def check_options(card_series, correct_options):
            computed_options = card_series.get_add_back_options()
            self.assertEqual(computed_options, correct_options, msg="{}".format(card_series))

        for suit in POSSIBLE_SUIT:
            check_options(card_series=CardSeries([Card(2, suit), Card(3, suit), Card(4, suit)]),
                          correct_options=[Card(5, suit), Card(JOKER_RANK, JOKER_SUIT), Card(2, suit)])
            check_options(card_series=CardSeries([Card(11, suit), Card(12, suit), Card(13, suit)]),
                          correct_options=[Card(1, suit), Card(JOKER_RANK, JOKER_SUIT), Card(2, suit)])
            check_options(card_series=CardSeries([Card(12, suit), Card(13, suit), Card(1, suit)]),
                          correct_options=[])
            check_options(card_series=CardSeries([Card(3, suit), Card(2, suit), Card(5, suit)]),
                          correct_options=[Card(6, suit)])
            check_options(card_series=CardSeries([Card(2, suit), Card(2, suit), Card(4, suit)]),
                          correct_options=[Card(5, suit)])
            check_options(card_series=CardSeries([Card(2, suit), Card(JOKER_RANK, JOKER_SUIT), Card(4, suit)]),
                          correct_options=[Card(5, suit)])
            check_options(card_series=CardSeries([Card(4, suit), Card(JOKER_RANK, JOKER_SUIT), Card(6, suit)]),
                          correct_options=[Card(7, suit)])
            check_options(card_series=CardSeries([Card(JOKER_RANK, JOKER_SUIT), Card(6, suit), Card(7, suit)]),
                          correct_options=[Card(8, suit)])
            check_options(card_series=CardSeries([Card(4, suit), Card(5, suit), Card(JOKER_RANK, JOKER_SUIT)]),
                          correct_options=[Card(7, suit)])
            check_options(card_series=CardSeries([Card(11, suit), Card(12, suit), Card(JOKER_RANK, JOKER_SUIT)]),
                          correct_options=[Card(1, suit)])

    def test_get_swap_joker_options(self):
        def check_swap_options(card_series, correct_options):
            computed_options = card_series.get_swap_joker_options()
            self.assertEqual(correct_options, computed_options, msg="{}".format(card_series))

        for suit in POSSIBLE_SUIT:
            check_swap_options(card_series=CardSeries([Card(2, suit), Card(3, suit), Card(4, suit)]),
                               correct_options=[])
            check_swap_options(card_series=CardSeries([Card(11, suit), Card(12, suit), Card(13, suit)]),
                               correct_options=[])
            check_swap_options(card_series=CardSeries([Card(1, suit), Card(2, suit), Card(3, suit)]),
                               correct_options=[])
            check_swap_options(card_series=CardSeries([Card(3, suit), Card(2, suit), Card(5, suit)]),
                               correct_options=[])
            check_swap_options(card_series=CardSeries([Card(2, suit), Card(2, suit), Card(4, suit)]),
                               correct_options=[])
            check_swap_options(card_series=CardSeries([Card(4, suit), Card(JOKER_RANK, JOKER_SUIT), Card(6, suit)]),
                               correct_options=[Card(5, suit)])
            check_swap_options(card_series=CardSeries([Card(JOKER_RANK, JOKER_SUIT), Card(6, suit), Card(7, suit)]),
                               correct_options=[Card(5, suit)])
            check_swap_options(card_series=CardSeries([Card(4, suit), Card(5, suit), Card(JOKER_RANK, JOKER_SUIT)]),
                               correct_options=[Card(6, suit)])
            check_swap_options(card_series=CardSeries([Card(12, suit), Card(13, suit), Card(JOKER_RANK, JOKER_SUIT)]),
                               correct_options=[Card(1, suit)])
            check_swap_options(card_series=CardSeries([Card(12, suit), Card(JOKER_RANK, JOKER_SUIT), Card(1, suit)]),
                               correct_options=[Card(13, suit)])

    def test_get_swap_two_options(self):
        def check_swap_options(card_series, correct_options):
            computed_options = card_series.get_swap_two_options()
            self.assertEqual(correct_options, computed_options, msg="{}".format(card_series))

        for suit in POSSIBLE_SUIT:
            check_swap_options(card_series=CardSeries([Card(2, suit), Card(3, suit), Card(4, suit)]),
                               correct_options=[])
            check_swap_options(card_series=CardSeries([Card(11, suit), Card(12, suit), Card(13, suit)]),
                               correct_options=[])
            check_swap_options(card_series=CardSeries([Card(1, suit), Card(2, suit), Card(3, suit)]),
                               correct_options=[])
            check_swap_options(card_series=CardSeries([Card(3, suit), Card(2, suit), Card(5, suit)]),
                               correct_options=[Card(4, suit)])
            check_swap_options(card_series=CardSeries([Card(2, suit), Card(2, suit), Card(4, suit)]),
                               correct_options=[Card(3, suit)])
            check_swap_options(card_series=CardSeries([Card(2, suit), Card(6, suit), Card(7, suit)]),
                               correct_options=[Card(5, suit)])
            check_swap_options(card_series=CardSeries([Card(10, suit), Card(11, suit), Card(2, suit)]),
                               correct_options=[Card(12, suit)])
            check_swap_options(card_series=CardSeries([Card(12, suit), Card(13, suit), Card(2, suit)]),
                               correct_options=[Card(1, suit)])
            check_swap_options(card_series=CardSeries([Card(12, suit), Card(2, suit), Card(1, suit)]),
                               correct_options=[Card(13, suit)])
            check_swap_options(card_series=CardSeries([Card(4, suit), Card(JOKER_RANK, JOKER_SUIT), Card(6, suit)]),
                               correct_options=[])
            check_swap_options(card_series=CardSeries([Card(JOKER_RANK, JOKER_SUIT), Card(6, suit), Card(7, suit)]),
                               correct_options=[])
            check_swap_options(card_series=CardSeries([Card(4, suit), Card(5, suit), Card(JOKER_RANK, JOKER_SUIT)]),
                               correct_options=[])
