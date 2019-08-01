from abc import ABCMeta, abstractmethod
from typing import Optional, List

from base.card import Card


class CardSet(metaclass=ABCMeta):
    """Base class for any list of cards."""

    @abstractmethod
    def description(self) -> str:
        raise NotImplementedError

    def __init__(self, cards: Optional[List[Card]] = None):
        self._cards = cards if cards is not None else []

    def __len__(self):
        return len(self._cards)

    def __contains__(self, item):
        return item in self._cards

    def __iter__(self):
        return self._cards.__iter__()

    def num_cards(self):
        return len(self._cards)

    def __repr__(self):
        repr_str = '{} ['.format(self.description())
        for card in sorted(self._cards):
            repr_str += repr(card) + ', '
        repr_str = repr_str[:-2]
        repr_str += ']'
        return repr_str

    def __str__(self):
        str_str = "{} [\n\t".format(self.description())
        for card in sorted(self._cards):
            str_str += str(card) + ', '
        str_str = str_str[:-2]
        str_str += "\n]"
        return str_str
