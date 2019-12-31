from typing import Optional

from base.card import Card
from base.cards.card_series import CardSeries
from base.utils.card_constants import POSSIBLE_SUIT, JOKER_SUIT, JOKER_RANK


def series_generator(min_length: int = 1, max_length: Optional[int] = None):
    """
    Generate all possible CardSeries with length in range(min_length, max_length + 1).
    """
    for suit in POSSIBLE_SUIT:
        yield from suit_series_generator(suit, min_length=min_length, max_length=max_length)


def suit_series_generator(suit: str, min_length: int = 1, max_length: Optional[int] = None):
    """
    Generate all possible CardSeries in the given suit with length in range(min_length, max_length + 1).
    """
    for ranks in ranks_list_generator(min_length=min_length, max_length=max_length):
        original_series = [Card(rank, suit) for rank in ranks]
        yield CardSeries(original_series)
        # Any card in the series can also be a joker
        for i in range(len(original_series)):
            yield CardSeries(original_series[:i] + [Card(JOKER_RANK, JOKER_SUIT)] + original_series[i+1:])
        # Any card in the series can also be a 2 of another suit
        for possible_suit in (set(POSSIBLE_SUIT) - {suit}):
            for i in range(len(original_series)):
                yield CardSeries(original_series[:i] + [Card(2, possible_suit)] + original_series[i+1:])
        # If the series doesn't contain the suits 2, then any card can also be a 2 of the suit itself
        if 2 not in ranks:
            for i in range(len(original_series)):
                yield CardSeries(original_series[:i] + [Card(2, suit)] + original_series[i + 1:])


def ranks_list_generator(min_length: int, max_length: Optional[int]):
    """Generate lists of all possible CardSeries ranks."""
    ranks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 1]
    max_length = max_length or len(ranks) - 1
    for length in range(min_length, max_length + 1):
        for i in range(0, len(ranks) - length + 1):
            yield ranks[i:i+length]
