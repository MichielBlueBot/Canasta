from typing import Union

from base.constants import Constants
from base.utils.card_constants import POSSIBLE_RANK, POSSIBLE_SUIT, JOKER_SUIT, JOKER_RANK, RANK_TRANSLATION, \
    RANK_TRANSLATION_SHORT, HEARTS, DIAMONDS, SPADES

"""This module provides the :class:`Card` object.
This module also has 5 constant attributes that help validate or string format
the :class:`Card` object: :attr:`POSSIBLE_SUIT`, :attr:`POSSIBLE_RANK`,
, :attr:`JOKER_SUIT`, :attr:`JOKER_RANK`, and :attr:`RANK_TRANSLATION`
"""


class Card(object):
    """A Card object"""

    #: Holds the suit as a lowercase string
    _suit = None

    #: Holds an integer which represents the card rank
    _rank = None

    def __init__(self, rank, suit):
        """
        :param int rank: a rank in :attr:`POSSIBLE_RANK` or :attr:`JOKER_RANK`
        :param str suit: a case-independent string in :attr:`POSSIBLE_SUIT` or
                         :attr:`JOKER_SUIT`
        :raises: ValueError
        """

        # convert to lowercase
        suit = suit.lower()

        base_error_str = 'A new Card cannot be created.'

        if suit == JOKER_SUIT:
            if rank == JOKER_RANK:
                self._suit = suit
                self._rank = rank
            else:
                raise ValueError(base_error_str + " Joker's rank must be %d" % JOKER_RANK)
        elif suit in POSSIBLE_SUIT:
            self._suit = suit

            if rank in POSSIBLE_RANK:
                self._rank = rank
            else:
                raise ValueError(base_error_str + " A normal card's rank (%s) is not %s." % (rank, POSSIBLE_RANK))
        else:
            raise ValueError(base_error_str + " Suit ('%s') is not in %s." % (suit, POSSIBLE_SUIT + [JOKER_SUIT]))

    def _translate_rank(self) -> Union[int, str]:
        """This is a hidden method that changes the card rank to a
        human-readable string. It also returns the title case of the string if
        possible.
        'Ace' for 1
        'Joker' for joker
        :returns: human-readable string for face cards or card rank
        :rtype: str
        """
        if self.is_joker():
            return JOKER_SUIT.title()
        elif self.get_rank() in RANK_TRANSLATION:
            return RANK_TRANSLATION[self.get_rank()].title()
        else:
            return self.get_rank()

    def _translate_rank_short(self) -> Union[int, str]:
        """This is a hidden method that changes the card rank to a short
        human-readable string.
        :returns: human-readable string for face cards or card rank
        :rtype: str
        """
        if self.is_joker():
            return "Joker"
        elif self.get_rank() in RANK_TRANSLATION_SHORT:
            return RANK_TRANSLATION_SHORT[self.get_rank()]
        else:
            return self.get_rank()

    def __repr__(self) -> str:
        """This method returns an unambigious string representation of the card object
        :returns: unambigious string representation of card object
        :rtype: str
        """
        return "Card(_rank=%s, _suit=%s)" % (self.get_rank(), self.get_suit())

    def __str__(self) -> str:
        """This method returns a short string representation of the card object
        useful in printing card object as "%s"
        :returns: human readable string representation of card object
        :rtype: str
        """
        translated_rank = self._translate_rank_short()
        if self.is_joker():
            return translated_rank
        else:
            return "%s-%s" % (translated_rank, self._suit[0].upper())

    def print(self):
        """This method returns a nice string representation of the card object
        useful in printing card object as "%s"
        :returns: human readable string representation of card object
        :rtype: str
        """
        translated_rank = self._translate_rank()
        if self.is_joker():
            return translated_rank
        else:
            return "%s of %s" % (translated_rank, self._suit.title())

    def get_rank(self) -> int:
        """
        :returns: :attr:`_rank`
        :rtype: int
        """
        return self._rank

    def get_suit(self) -> str:
        """
        :returns: :attr:`_suit`
        :rtype: str
        """
        return self._suit

    def get_score(self):
        """Return the value of this card in the scoring of the game."""
        if self.is_joker():  # Joker
            return Constants.JOKER_VALUE
        if self.get_rank() == 1:  # Ace
            return Constants.ACE_VALUE
        if self.get_rank() <= 7:  # 3, 4, 5, 6, 7
            return Constants.LOW_CARD_VALUE
        else:  # 8, 9, 10, J, Q, K and 2
            return Constants.HIGH_CARD_VALUE

    def is_joker_like(self) -> bool:
        """
        :returns: True if joker or two
        :rtype: bool
        """
        return self.is_two() or self.is_joker()

    def is_joker(self) -> bool:
        """
        :returns: True if joker
        :rtype: bool
        """
        return (JOKER_RANK == self.get_rank()) and (JOKER_SUIT == self.get_suit())

    def is_two(self) -> bool:
        """
        :returns: True if two
        :rtype: bool
        """
        return 2 == self.get_rank()

    def _key(self):
        return self._rank, self._suit

    def __hash__(self):
        return hash(self._key())

    def __eq__(self, other) -> bool:
        """Override equality method
        :returns: True if two objects are cards and have the same :attr:`_rank` and :attr:`_suit`
        :rtype: bool
        """
        if type(other) is type(self):
            if self._key() == other._key():
                return True
        return False

    def __ne__(self, other) -> bool:
        """Override inequality method
        :returns: not :attr:`__eq__`
        :rtype: bool
        """
        return not self.__eq__(other)

    def __lt__(self, other: 'Card') -> bool:
        if self.is_joker():
            return True
        if other.is_joker():
            return False
        self_suit = self.get_suit()
        other_suit = other.get_suit()
        if self_suit == other_suit:
            return self.get_rank() < other.get_rank()
        else:
            if self_suit == HEARTS:
                return True
            elif other_suit == HEARTS:
                return False
            elif self_suit == DIAMONDS:
                return True
            elif other_suit == DIAMONDS:
                return False
            elif self_suit == SPADES:
                return True
            else:
                return False
