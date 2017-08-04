#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import datetime

from typing import List

logger = logging.getLogger(__name__)


def aggregate(times: List[datetime.datetime], errorRange: float) -> List[datetime.datetime]:
    tmp = []
    features = []
    for idx, time in enumerate(times):
        if len(features) > 0:
            minFeature = features[0] - datetime.timedelta(seconds=errorRange*60)
            maxFeature = features[0] + datetime.timedelta(seconds=errorRange*60)
            if minFeature <= time and maxFeature >= time:
                features.append(time)
            else:
                tmp.append(features[int(len(features)/2)])
                features = []
        elif idx == len(times) - 1:
            tmp.append(time)
        else:
            features.append(time)
    return tmp
