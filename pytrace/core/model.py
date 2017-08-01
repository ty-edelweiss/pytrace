#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from typing import List, Tuple

class TraceModel(object):

    def __init__(self, windows: List[Tuple[datetime.datetime, datetime.datetime]], coefficients: List[int]):
        self.clusters_ = windows
        self.coefficients_ = coefficients

    def evaluate(self, subject: datetime.datetime) -> int:
        result = float("nan")
        for idx, cluster in enumerate(self.clusters_):
            if cluster[0] <= subject and cluster[1] >= subject:
                result = self.coefficients_[idx]
                break
            else:
                continue
        return result

    def predict(self, features: List[datetime.datetime], mode: str = "all") -> List[int]:
        predicts = [self.evaluate(feature) for feature in features]
        return predicts
