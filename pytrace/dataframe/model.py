#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import pandas as pd

from typing import List

from ..core.model import TraceModel as TraceModelCore
from ..wrapper.pandas import predict_dataframe_wrapper


class TraceModel(TraceModelCore):

    @predict_dataframe_wrapper
    def predict(self, features: List[datetime.datetime], mode: str = "all") -> List[int]:
        return super().predict(features, mode)
