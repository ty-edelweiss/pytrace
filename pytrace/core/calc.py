#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from typing import List, Tuple

class CalcTrace(object):

    def __init__(self, span: float = 180.0, precision: float = 30.0, bandwidth: float = 1440.0):
        self.span_ = span * 60.0
        self.precision_ = precision * 60.0
        self.bandwidth_ = bandwidth * 60.0

    def window(self, ref_time: datetime.datetime, coef_value: int, reverse: bool = False) -> Tuple[Tuple[datetime.datetime, datetime.datetime], int]:
        if coef_value >= 0:
            centroid = ref_time + datetime.timedelta(seconds=self.span_ * coef_value)
        else:
            centroid = ref_time - datetime.timedelta(seconds=self.span_ * abs(coef_value))
        trace = (centroid - datetime.timedelta(seconds=self.precision_), centroid + datetime.timedelta(seconds=self.precision_))
        return trace, coef_value

    def calc(self, times: List[datetime.datetime], ref_time: datetime.datetime) -> List[Tuple[Tuple[datetime.datetime, datetime.datetime], int]]:
        traces = []
        time_series = sorted(times)
        window_numbers = int(self.bandwidth_ / self.span_)
        if ref_time is None:
            ref_time = time_series[0]
            traces.append(((ref_time, ref_time), 0))
            traces.extend([self.window(ref_time, n) for n in range(1, window_numbers + 1)])
        else:
            traces.extend([self.window(ref_time, n, True) for n in range(-window_numbers, 0)])
            traces.append(((ref_time, ref_time), 0))
            traces.extend([self.window(ref_time, n) for n in range(1, window_numbers + 1)])
        return traces
