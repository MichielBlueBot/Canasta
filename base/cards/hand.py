from typing import Union, List, Optional

from base.card import Card
from base.cards.card_set import CardSet


class Hand(CardSet):

    def description(self) -> str:
        return "Hand"

    def add(self, cards: Union[Card, List[Card]]):
        if isinstance(cards, Card):
            self._cards.append(cards)
        else:
            self._cards.extend(cards)

    def pop(self, card: Card) -> Card:
        if card in self._cards:
            self._cards.remove(card)
        return card

    def is_empty(self) -> bool:
        return len(self._cards) == 0
