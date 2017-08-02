#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Callable, List

import pandas as pd
from ..core.trace import Tracer
from ..core.model import TraceModel

def fit_dataframe_wrapper(func: Callable[[Tracer, List[float]], TraceModel]) -> Callable[[Tracer, pd.core.frame.DataFrame, str], TraceModel]:
    import functools
    @functools.wraps(func)
    def _wrap(self, dataframe: pd.core.frame.DataFrame, featureCol: str = "features", **kwargs) -> TraceModel:
        features = [dt.to_pydatetime() for idx, dt in dataframe[featureCol].iteritems()]
        return func(self, features, **kwargs)
    return _wrap

def predict_dataframe_wrapper(func: Callable[[Tracer, List[float]], List[float]]) -> Callable[[Tracer, pd.core.frame.DataFrame, str], pd.core.frame.DataFrame]:
    import functools
    @functools.wraps(func)
    def _wrap(self, dataframe: pd.core.frame.DataFrame, featureCol: str = "features", predictCol: str = "labels", **kwargs) -> pd.core.frame.DataFrame:
        features = [dt.to_pydatetime() for idx, dt in dataframe[featureCol].iteritems()]
        predictions = func(self, features, **kwargs)
        newframe = pd.Series(predictions, index=dataframe.index.tolist(), name=predictCol)
        return pd.concat([dataframe, newframe], axis=1)
    return _wrap
