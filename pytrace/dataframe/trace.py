#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import pandas as pd

from typing import List

from .model import TraceModel
from ..core.trace import Tracer as TracerCore
from ..wrapper.pandas import fit_dataframe_wrapper


class Tracer(TracerCore):

    @fit_dataframe_wrapper
    def fit(self, X: List[datetime.datetime]) -> TraceModel:
        core_model = super().fit(X)
        return TraceModel(core_model.clusters_)
