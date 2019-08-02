from typing import List, Union
import numpy as np
from sklearn.preprocessing import MultiLabelBinarizer

from base.card import Card
from base.card_constants import POSSIBLE_SUIT, POSSIBLE_RANK, JOKER_SUIT, JOKER_RANK


class CardEncoder:

    def __init__(self):
        classes = [Card(rank, suit) for suit in POSSIBLE_SUIT for rank in POSSIBLE_RANK]+[Card(JOKER_RANK, JOKER_SUIT)]
        self.encoder = MultiLabelBinarizer(classes=classes)

    def encode(self, cards: Union[Card, List[Card]]) -> np.ndarray:
        if isinstance(cards, Card):
            cards = [cards]
        return self.encoder.fit_transform([cards])[0]
