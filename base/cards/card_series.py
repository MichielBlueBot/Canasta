from typing import List

from base.card import Card, JOKER_RANK, JOKER_SUIT
from base.cards.card_set import CardSet
from base.enums.two_swap_direction import TwoSwapDirection


class CardSeries(CardSet):
    """A series of cards played by a team on the board. E.g: [3H-2H-5H-6H-7H] """

    def description(self) -> str:
        return "CardSeries"

    def get_raw_cards(self) -> List[Card]:
        return self._cards

    def get_card(self, index: int) -> Card:
        return self._cards[index]

    def get_add_front_options(self) -> List[Card]:
        options = []
        if self._cards:
            first_card = self._cards[0]
            if not first_card.is_joker() or self.is_two_joker(0):
                rank = first_card.get_rank()
                if rank != 1:
                    options.append(Card(rank - 1, first_card.get_suit()))
            else:
                second_card = self._cards[1]
                if not second_card.get_rank() == 2:  # Can only prepend joker if its not for the ACE
                    options.append(Card(second_card.get_rank() - 2, second_card.get_suit()))
                else:
                    # Special case of [2, 2, 4, ...] which can be prepended by the ace
                    third_card = self._cards[2]
                    if third_card.get_rank() == 4:
                        options.append(Card(1, third_card.get_suit()))
            if not first_card.get_rank() == 1 and not self.has_joker() and not self.has_two_joker():
                # We can add jokers if there isn't one yet
                options.append(Card(JOKER_RANK, JOKER_SUIT))
                options.append(Card(2, first_card.get_suit()))
        return options

    def get_add_back_options(self) -> List[Card]:
        options = []
        if self._cards:
            last_card = self._cards[-1]
            if not last_card.is_joker() or self.is_two_joker(-1):
                rank = last_card.get_rank()
                if rank == 13:  # After king comes ACE
                    options.append(Card(1, last_card.get_suit()))
                elif rank != 1:  # After everything else comes rank + 1
                    options.append(Card(rank + 1, last_card.get_suit()))
            else:
                second_last_card = self._cards[-2]
                if second_last_card.get_rank() == 12:  # [..., queen, joker]
                    options.append(Card(1, second_last_card.get_suit()))
                elif second_last_card.get_rank() != 13:
                    options.append(Card(second_last_card.get_rank() + 2, second_last_card.get_suit()))
            if not last_card.get_rank() == 1 and not self.has_joker() and not self.has_two_joker():
                # We can add jokers if there isn't one yet
                options.append(Card(JOKER_RANK, JOKER_SUIT))
                options.append(Card(2, last_card.get_suit()))
        return options

    def get_swap_joker_options(self) -> List[Card]:
        options = []
        for i, card in enumerate(self._cards):
            if card.is_joker():
                if i == 0:
                    # There has to be a next card
                    next_card = self._cards[i + 1]
                    if next_card.get_rank() == 1:  # Joker is in the King position
                        options.append(Card(13, next_card.get_suit()))
                    else:  # Joker rank is one less than the next card
                        options.append(Card(next_card.get_rank() - 1, next_card.get_suit()))
                else:
                    # There has to be a previous card
                    previous_card = self._cards[i - 1]
                    if previous_card.get_rank() == 13:  # Joker is in the back-ace position
                        options.append(Card(1, previous_card.get_suit()))
                    else:  # Joker rank is one higher than the previous card
                        options.append(Card(previous_card.get_rank() + 1, previous_card.get_suit()))
        return options

    def get_swap_two_options(self) -> List[Card]:
        options = []
        for i, card in enumerate(self._cards):
            if self.is_two_joker(i):
                if i == 0:
                    # There has to be a next card
                    next_card = self._cards[i + 1]
                    if next_card.get_rank() == 1:  # Two is in the King position
                        options.append(Card(13, next_card.get_suit()))
                    else:  # Two rank is one less than the next card
                        options.append(Card(next_card.get_rank() - 1, next_card.get_suit()))
                else:
                    # There has to be a previous card
                    previous_card = self._cards[i - 1]
                    if previous_card.get_rank() == 13:  # Two is in the back-ace position
                        options.append(Card(1, previous_card.get_suit()))
                    else:  # Two rank is one higher than the previous card
                        options.append(Card(previous_card.get_rank() + 1, previous_card.get_suit()))
        return options

    def add_front(self, card: Card):
        self._cards = [card] + self._cards

    def add_back(self, card: Card):
        self._cards.append(card)

    def swap_joker(self, swap_card: Card):
        new_cards = []
        joker = None
        for card in self._cards:
            if card.is_joker():
                joker = card
                new_cards.append(swap_card)
            else:
                new_cards.append(card)
        self._cards = new_cards
        return joker

    def swap_two(self, swap_card: Card, direction: TwoSwapDirection = TwoSwapDirection.FRONT) -> None:
        new_cards = []
        two = None
        for i, card in enumerate(self._cards):
            if self.is_two_joker(i):
                two = card
                new_cards.append(swap_card)
            else:
                new_cards.append(card)
        self._cards = new_cards
        if direction == TwoSwapDirection.FRONT:
            self.add_front(two)
        elif direction == TwoSwapDirection.BACK:
            self.add_back(two)
        else:
            raise Exception("Invalid two-swap-direction, use TwoSwapDirection enum!")

    def has_joker(self) -> bool:
        for card in self._cards:
            if card.is_joker():
                return True
        return False

    def has_two_joker(self) -> bool:
        num_cards = len(self._cards)
        for i, card in enumerate(self._cards):
            if card.is_two():
                if i < num_cards - 1:
                    next_card = self._cards[i + 1]
                    if next_card.get_rank() == 3:
                        # Found a two but it's in the proper spot
                        return False
                    else:
                        # Found a two and it's not in the proper spot, so its a joker
                        return True
                if i > 0:
                    previous_card = self._cards[i - 1]
                    if previous_card.get_rank() == 1:
                        # Found a two but it's in the proper spot
                        return False
                    else:
                        # Found a two and it's not in the proper spot, so its a joker
                        return True
        # No two card found
        return False

    def is_two_joker(self, i: int) -> bool:
        """
        :return True if the card at the given index is a two-joker.
        """
        card = self.get_card(i)
        if card.is_two():
            if i > 0:
                previous_card = self.get_card(i - 1)
                if previous_card.get_rank() == 1:
                    return False  # preceded by ace, not a joker
            if i < len(self) - 1:
                next_card = self.get_card(i + 1)
                if next_card.get_rank() == 3:
                    return False  # proceeded by 3, not a joker
                if i < len(self) - 2:
                    next_next_card = self.get_card(i + 2)
                    if next_next_card.get_rank() == 4:
                        return False  # first two in [2, 2, 4, ...], not a joker
            return True  # its a joker
        return False

    def is_dirty(self) -> bool:
        """Return True if this series is dirty."""
        return self.num_cards() >= 7 and (self.has_joker() or self.has_two_joker())

    def is_pure(self) -> bool:
        """Return True if this series is pure."""
        return self.num_cards() >= 7 and not self.has_joker() and not self.has_two_joker()

    def is_five_hundred(self) -> bool:
        """Return True if this series is a 500-series."""
        return self.num_cards() == 12 and not self.has_joker() and not self.has_two_joker()

    def is_thousand(self) -> bool:
        """Return True if this series is a 1000-series."""
        return self.num_cards() == 13 and not self.has_joker() and not self.has_two_joker()

    def is_valid(self) -> bool:
        # Make sure all non-joker and non-two cards have the same suit
        if not self._check_valid_suits():
            return False
        # Make sure the series contains at most one joker
        if not self._check_valid_num_jokers():
            return False
        # Make sure all cards follow each other, allowing for jokers
        if not self._check_valid_card_sequence():
            return False
        return True

    def _check_valid_suits(self) -> bool:
        suits = [card.get_suit() for card in self._cards if not card.is_joker_like()]
        if not self._check_equal(suits):
            return False
        return True

    def _check_valid_num_jokers(self) -> bool:
        num_jokers = 0
        for i in range(len(self._cards)):
            card = self._cards[i]
            if card.is_joker():
                num_jokers += 1
            elif card.is_two():
                if i > 0 and self._cards[i - 1].get_rank() == 1:
                    continue  # If the two is preceded by an ACE, its not a joker
                elif i < len(self._cards) - 1 and self._cards[i + 1].get_rank() == 3:
                    continue  # If the two is proceeded by a 3, its not a joker
                elif i < len(self._cards) - 2 and self._cards[i + 1].is_two() and self._cards[i + 2].get_rank() == 4:
                    continue  # in a [..., 2, 2, 4, ...] series the first two is not a joker
                else:
                    # otherwise, this two is a joker
                    num_jokers += 1
        return num_jokers <= 1

    def _check_valid_card_sequence(self):
        pre_previous_card = None
        previous_card = None
        for card in self._cards:
            if previous_card is not None:
                if previous_card.is_joker() or previous_card.is_two():
                    if pre_previous_card is not None:
                        if pre_previous_card.get_rank() + 2 != card.get_rank():
                            # The pre-previous card rank should be 2 behind the current card rank
                            # pre-previous | joker or two | current
                            return False
                if not (previous_card.is_joker_like() or card.is_joker_like()):
                    if previous_card.get_rank() + 1 != card.get_rank():
                        return False
                pre_previous_card = previous_card
            previous_card = card
        return True

    @staticmethod
    def _check_equal(iterator):
        iterator = iter(iterator)
        try:
            first = next(iterator)
        except StopIteration:
            return True
        return all(first == rest for rest in iterator)

    def __repr__(self):
        repr_str = '{} ['.format(self.description())
        for card in self._cards:
            repr_str += repr(card) + ', '
        repr_str = repr_str[:-2]
        repr_str += ']'
        return repr_str
