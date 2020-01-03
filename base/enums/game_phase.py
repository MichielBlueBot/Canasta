from enum import Enum


class GamePhase(Enum):

    DRAW_PHASE = 0  # initial player turn phase, drawing a card from the deck or grabbing the stack
    ACTION_PHASE = 1  # default player turn phase, player execution any number of actions on the board
    PLAY_JOKER_PHASE = 2  # player has just swapped a joker and needs to put it back into play
    NO_CARDS_PHASE = 3  # player has no cards left and is in position to grab one of the piles or end the game
    NO_CARDS_END_TURN_PHASE = 4  # player has no cards left after discarding, it may grab a pile but its turn is over
    END_TURN_PHASE = 5  # phase that ends a players turn
    EMPTY_DECK_GAME_END_PHASE = 6  # phase that occurs when there are no cards left to play in the deck and no piles left to use
