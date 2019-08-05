from collections import Counter
from typing import List, Union

import numpy as np
from sklearn.preprocessing import MultiLabelBinarizer

from base.cards.card_series import CardSeries
from base.utils.generators import series_generator


class CardSeriesEncoder:

    def __init__(self):
        classes = list(series_generator(min_length=3))
        self.encoder = MultiLabelBinarizer(classes=classes)

    def encode(self, series: Union[CardSeries, List[CardSeries]]) -> np.ndarray:
        if isinstance(series, CardSeries):
            series = [series]
        return self.encoder.fit_transform([series])[0]
