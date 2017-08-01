#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from typing import List

from .calc import CalcTrace
from .model import TraceModel


class Tracer(CalcTrace):

    def __init__(self, span: float = 180.0, precision: float = 30.0, bandwidth: float = 1440.0):
        super().__init__(span, precision, bandwidth)

    def setSpan(self, span: float) -> object:
        self.span_ = span
        return self

    def setPrecision(self, precision: float) -> object:
        self.precision_ = precision
        return self

    def setBandWidth(self, bandwidth: float) -> object:
        self.bandwidth_ = bandwidth
        return self

    def getSpan(self) -> float:
        return self.span_

    def getPrecision(self) -> float:
        return self.precision_

    def getBandWidth(self) -> float:
        return self.bandwidth_

    def fit(self, X: List[datetime.datetime], ref: datetime.datetime = None) -> TraceModel:
        features = super().calc(X, ref)
        windows = [feature[0] for feature in features]
        coefficients = [feature[1] for feature in features]
        model = TraceModel(windows, coefficients)
        return model
