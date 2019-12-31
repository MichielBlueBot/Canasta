class Constants:

    NUM_CARDS_IN_STARTING_HAND = 11
    NUM_CARDS_IN_PILE = 11
    NUM_PLAYERS = 4     # Variable only for readability, cannot be altered
    NUM_TEAMS = 2       # Variable only for readability, cannot be altered
    AI_PLAYER_INDEXES = [1, 2, 3]
    HUMAN_PLAYER_INDEXES = [0]

    DIRTY_SCORE = 100
    PURE_SCORE = 200
    FIVE_HUNDRED_SCORE = 500
    THOUSAND_SCORE = 1000

    TAKE_PILE_VALUE = 100  # Value for a team taking their pile

    LOW_CARD_VALUE = 5
    HIGH_CARD_VALUE = 10
    ACE_VALUE = 15
    JOKER_VALUE = 20
    JOKER_SWAP_EXTRA_SCORE = 40  # When swapping a joker, the value of a series might go down, so we add this score to add incentive

    GAME_ID_LENGTH = 20
