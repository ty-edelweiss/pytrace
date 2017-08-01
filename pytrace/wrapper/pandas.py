#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Callable, List

import pandas as pd
from ..core.track import Track
from ..core.model import TrackModel

def fit_dataframe_wrapper(func: Callable[[Track, List[float]], TrackModel]) -> Callable[[Track, pd.core.frame.DataFrame, str], TrackModel]:
    import functools
    @functools.wraps(func)
    def _wrap(self, dataframe: pd.core.frame.DataFrame, featureCol: str = "features", **kwargs) -> TrackModel:
        features = [dt.to_pydatetime() for idx, dt in dataframe[featureCol].iteritems()]
        return func(self, features, **kwargs)
    return _wrap

def predict_dataframe_wrapper(func: Callable[[Track, List[float]], List[float]]) -> Callable[[Track, pd.core.frame.DataFrame, str], pd.core.frame.DataFrame]:
    import functools
    @functools.wraps(func)
    def _wrap(self, dataframe: pd.core.frame.DataFrame, featureCol: str = "features", predictCol: str = "labels", **kwargs) -> pd.core.frame.DataFrame:
        features = [dt.to_pydatetime() for idx, dt in dataframe[featureCol].iteritems()]
        predictions = func(self, features, **kwargs)
        newframe = pd.Series(predictions, index=dataframe.index.tolist(), name=predictCol)
        return pd.concat([dataframe, newframe], axis=1)
    return _wrap
