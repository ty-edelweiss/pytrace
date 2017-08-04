#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import pandas
from prettytable import PrettyTable

from typing import List, Tuple, Any

logger = logging.getLogger(__name__)

def cast(datum: Any, type: str) -> Any:
    if type == "int":
        return int(datum)
    elif type == "float":
        return float(datum)
    elif type == "string":
        return str(datum)
    else:
        return datum

def all(dataframe: pandas.core.frame.DataFrame, displayCol: List[str]):
    pandas.set_option('display.max_rows', len(dataframe))
    print(dataframe[displayCol])
    pandas.reset_option('display.max_rows')


def flow(dataframe: pandas.core.frame.DataFrame, span: float, displayCol: List[str], featureCol: str, predictCol: str = "labels", types: List[str] = None):
    minLabel = int(dataframe[predictCol].min())
    maxLabel = int(dataframe[predictCol].max())
    headers = ["Chart", "Trace Flow"] + [header[0].upper() + header[1:].replace("_", "-") for header in displayCol]
    table = PrettyTable(headers)
    for header in headers:
        if header == "Chart" or header == "Trace Flow":
            table.align[header] = "c"
        else:
            table.align[header] = "r"
    for label in range(minLabel, maxLabel+1):
        feature_series = dataframe[dataframe[predictCol] == label]
        if label == 0:
            time = feature_series[featureCol].tolist()[0]
            extras = feature_series[displayCol].values.tolist()[0]
            if types is None:
                values = ["*", time] + extras
            else:
                values = ["*", time] + [cast(extra, type) for extra, type in zip(extras, types)]
            table.add_row(values)
        else:
            if len(feature_series) > 0:
                time = feature_series[featureCol].tolist()[0]
                extras = feature_series[displayCol].values.tolist()[0]
                if types is None:
                    values = [str(label), time] + extras
                else:
                    values = [str(label), time] + [cast(extra, type) for extra, type in zip(extras, types)]
                table.add_row(values)
            else:
                values = [str(label), "x"] + ["x" for _ in displayCol]
                table.add_row(values)
        if label != maxLabel:
            values = ["↓  + {0:02d}:{1:02d}:00".format(int(span/60.0), int(span%60.0)), ""] + ["" for _ in displayCol]
            table.add_row(values)
    print(table)
