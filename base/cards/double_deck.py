import logging

from base.card import Card, JOKER_RANK, JOKER_SUIT, POSSIBLE_RANK, POSSIBLE_SUIT
from base.cards.deck import Deck

#: a logger object
LOGGER = logging.getLogger(__name__)


class DoubleDeck(Deck):
    """A DoubleDeck object
        A new double deck starts out ordered.
        If jokers are included, contains 2 * (2 + 4 * 13) :class:`deck_of_cards.card.Card` objects
        If no jokers are included, contains 2 * (4 * 13) :class:`deck_of_cards.card.Card` objects
        """

    def __init__(self, with_jokers=True):
        """
        :param bool with_jokers: include jokers if True
        """
        super().__init__(with_jokers=with_jokers)
        # Add another deck of cards
        if with_jokers:
            for _ in range(2):
                self._cards.append(Card(JOKER_RANK, JOKER_SUIT))

        for suit in POSSIBLE_SUIT:
            for rank in POSSIBLE_RANK:
                self._cards.append(Card(rank, suit))

    def check_deck(self):
        """Check to make sure all the cards are accounted
        :returns: True if all cards are accounted
        :rtype: bool
        """

        # start with a simple card count check
        total_possible_cards = 2 * ((13 * 4) + (2 if self._with_jokers else 0))
        if total_possible_cards != (len(self._cards)
                                    + len(self._in_play_cards)
                                    + len(self._discarded_cards)):
            return False

        return_value = True

        # go through all piles of cards and create a dictionary with
        # [suit][rank] = number of occurrences of card
        card_dict = {}
        for pile in [self._cards, self._in_play_cards, self._discarded_cards]:
            for c_card in pile:
                suit = c_card.get_suit()
                rank = c_card.get_rank()

                if suit not in card_dict:
                    card_dict[suit] = {}

                if rank not in card_dict[suit]:
                    card_dict[suit][rank] = 1
                else:
                    card_dict[suit][rank] += 1

        # go through generated card_dictionary to make sure that there are the
        # appropriate rank of occurrences for each card
        for suit in card_dict.keys():
            for rank in card_dict[suit].keys():
                if 4 == card_dict[suit][rank]:
                    # check for 4 jokers
                    if not (JOKER_SUIT == suit and JOKER_RANK == rank):
                        return_value = False
                elif 2 != card_dict[suit][rank]:
                    LOGGER.info("Something is wrong with the %s", Card(rank, suit))
                    return_value = False

        return return_value
