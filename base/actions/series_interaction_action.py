from abc import ABCMeta
from numbers import Number

from base.actions.action import Action
from base.cards.card_series import CardSeries


class SeriesInteractionAction(Action, metaclass=ABCMeta):
    """Subclass of actions that interact with a series."""

    def __init__(self, series: CardSeries):
        super().__init__()
        self.series = series
        self.score_value = None  # The added value to the teams score by performing this action

    def get_reward(self) -> Number:
        """
        Return the reward for executing this action.

        The rewards for series interaction actions are computed by storing the value of the series before- and after execution.
        The reward is equal to the increase in the series value as a result of this action.
        This means that the reward is only available after the action has been executed.
        """
        if self.is_executed:
            return self.score_value
        else:
            raise NotImplementedError("Reward for this action is not implemented if the action is not yet executed.")
