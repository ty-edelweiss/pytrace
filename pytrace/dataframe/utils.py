#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import datetime
import pandas as pd

logger = logging.getLogger(__name__)


def aggregate(dataframe: pd.core.frame.DataFrame, featureCol: str, errorRange: float) -> pd.core.frame.DataFrame:
    tmp = []
    features = []
    columns = tuple(dataframe.columns.values)
    for idx, row in dataframe.sort_values(by=[featureCol], ascending=True).iterrows():
        time = row[featureCol].to_pydatetime()
        if len(features) > 0:
            ref = features[0][featureCol].to_pydatetime()
            maxFeature = ref + datetime.timedelta(seconds=errorRange*60)
            if maxFeature >= time:
                features.append(row)
            else:
                tmp.append(tuple(features[int(len(features)/2)].tolist()))
                features = [ row ]
        else:
            features.append(row)
    if len(features) > 0:
        tmp.append(tuple(features[int(len(features)/2)].tolist()))
    newframe = pd.DataFrame(tmp, columns=columns)
    return newframe


def aggregate2(dataframe: pd.core.frame.DataFrame, featureCol: str, subfeatureCol: str, errorRange: float) -> pd.core.frame.DataFrame:
    tmp = []
    features = []
    columns = tuple(dataframe.columns.values)
    for idx, row in dataframe.sort_values(by=[featureCol], ascending=True).iterrows():
        time = row[featureCol].to_pydatetime()
        sub_value = row[subfeatureCol]
        if len(features) > 0:
            ref = features[0][featureCol].to_pydatetime()
            maxFeature = ref + datetime.timedelta(seconds=errorRange*60)
            subFeature = features[0][subfeatureCol]
            if maxFeature >= time:
                if sub_value != subFeature:
                    tmp.append(tuple(features[int(len(features)/2)].tolist()))
                    features = [ row ]
                else:
                    features.append(row)
            else:
                tmp.append(tuple(features[int(len(features)/2)].tolist()))
                features = [ row ]
        else:
            features.append(row)
    if len(features) > 0:
        tmp.append(tuple(features[int(len(features)/2)].tolist()))
    newframe = pd.DataFrame(tmp, columns=columns)
    return newframe
