from typing import List, TYPE_CHECKING, Optional

from base.card import Card
from base.card_constants import POSSIBLE_SUIT, JOKER_SUIT, JOKER_RANK, POSSIBLE_RANK
from base.cards.card_series import CardSeries
from base.enums.pile_side import PileSide
from base.enums.two_swap_direction import TwoSwapDirection

from base.actions.action import Action
from base.actions.add_back_action import AddBackAction
from base.actions.add_front_action import AddFrontAction
from base.actions.discard_card_action import DiscardCardAction
from base.actions.put_action import PutAction
from base.actions.swap_joker_action import SwapJokerAction
from base.actions.take_card_action import TakeCardAction
from base.actions.swap_two_action import SwapTwoAction
from base.actions.take_pile_action import TakePileAction
from base.actions.take_stack_action import TakeStackAction


def get_take_card_actions() -> List['Action']:
    yield TakeCardAction()


def get_take_pile_actions() -> List['Action']:
    yield TakePileAction(PileSide.LEFT)
    yield TakePileAction(PileSide.RIGHT)


def get_take_stack_actions() -> List['Action']:
    yield TakeStackAction()


def get_swap_joker_actions() -> List['Action']:
    for series in series_generator(min_length=3, max_length=13):
        if series.has_joker():
            options = series.get_swap_joker_options()
            for option in options:
                yield SwapJokerAction(card=option, series=series)


def get_swap_two_actions() -> List['Action']:
    for series in series_generator(min_length=3, max_length=13):
        if series.has_two_joker():
            options = series.get_swap_two_options()
            for option in options:
                # We cannot put the two-joker to the front if either:
                #    - There is an ace in front of the series
                #    - We are replacing the two joker in the front-ace position with a real ace
                if series.get_card(0).get_rank() != 1 and (option.get_rank() != 1 or not series.is_two_joker(0)):
                    yield SwapTwoAction(card=option, series=series, direction=TwoSwapDirection.FRONT)
                # We cannot put the two-joker to the back if either:
                #    - There is an ace in the back of the series
                #    - We are replacing the two joker in the back-ace position with a real ace
                if series.get_card(-1).get_rank() != 1 and (option.get_rank() != 1 or not series.is_two_joker(-1)):
                    yield SwapTwoAction(card=option, series=series, direction=TwoSwapDirection.BACK)


def get_put_actions() -> List['Action']:
    for series in series_generator(min_length=3, max_length=13):
        yield PutAction(cards=series.get_raw_cards())


def get_discard_card_actions() -> List['Action']:
    yield DiscardCardAction(card=Card(JOKER_RANK, JOKER_SUIT))
    for suit in POSSIBLE_SUIT:
        for rank in POSSIBLE_RANK:
            yield(DiscardCardAction(card=Card(rank, suit)))


def get_add_front_actions() -> List['Action']:
    for series in series_generator(min_length=3, max_length=13):
        add_front_options = series.get_add_front_options()
        for option in add_front_options:
            yield AddFrontAction(card=option, series=series)


def get_add_back_actions() -> List['Action']:
    for series in series_generator(min_length=3, max_length=13):
        add_back_options = series.get_add_back_options()
        for option in add_back_options:
            yield AddBackAction(card=option, series=series)


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
        for i in range(len(original_series)):
            yield CardSeries(original_series[:i] + [Card(JOKER_RANK, JOKER_SUIT)] + original_series[i+1:])


def ranks_list_generator(min_length: int, max_length: Optional[int]):
    """Generate lists of all possible CardSeries ranks."""
    ranks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 1]
    max_length = max_length or len(ranks) - 1
    for length in range(min_length, max_length + 1):
        for i in range(0, len(ranks) - length + 1):
            yield ranks[i:i+length]
    if max_length == len(ranks):
        yield ranks


ALL_ACTIONS = (list(get_take_card_actions()) +
               list(get_take_pile_actions()) +
               list(get_take_stack_actions()) +
               list(get_swap_joker_actions()) +
               list(get_swap_two_actions()) +
               list(get_put_actions()) +
               list(get_discard_card_actions()) +
               list(get_add_front_actions()) +
               list(get_add_back_actions()))  # type: List['Action']
