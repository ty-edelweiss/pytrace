#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import pandas

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

def csv(dataframe: pandas.core.frame.DataFrame, targetCol: List[str]):
    pandas.set_option('display.max_rows', len(dataframe))
    print(dataframe[targetCol])
    pandas.reset_option('display.max_rows')


def flow(dataframe: pandas.core.frame.DataFrame, span: float, targetCol: List[str], featureCol: str, predictCol: str = "labels", types: List[str] = None):
    minLabel = int(dataframe[predictCol].min())
    maxLabel = int(dataframe[predictCol].max())
    headers = ["Chart", "Trace Flow"] + [header[0].upper() + header[1:].replace("_", "-") for header in displayCol]
