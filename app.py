#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import logging.handlers
from optparse import OptionParser

import psycopg2
import pandas as pd

from pytrace import display
from pytrace.dataframe.trace import Tracer

VENDOR = "flickr"
LOG_FORMAT = "%(asctime)s %(levelname)s %(name)s: %(message)s"

parser = OptionParser()

parser.add_option(
    "-d", "--dimension",
    choices=[4, 5, 6],
    default=4,
    help="dimension of mesh code",
    dest="dimension"
)

parser.add_option(
    "-m", "--mesh",
    type="int",
    dest="mesh"
)

parser.add_option(
    "-t", "--target",
    type="string",
    dest="target"
)

parser.add_option(
    "-s", "--span",
    type="float",
    defaut=180.0,
    dest="span"
)

parser.add_option(
    "-b", "--bandwidth",
    type="float",
    default=30.0,
    dest="bandwidth"
)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(logging.Formatter(LOG_FORMAT))

file_handler = logging.handlers.RotatingFileHandler(
    filename="./logs/app.log",
    maxBytes=1000,
    backupCount=3,
    encoding="utf-8"
)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter(LOG_FORMAT))

logging.getLogger().addHandler(stream_handler)
logging.getLogger().addHandler(file_handler)
logging.getLogger().setLevel(logging.DEBUG)

if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    options, args = parser.parse_args()

    target = options["target"]
    target_mesh = options["mesh"]
    table_name = VENDOR + "_mesh_" + options["dimension"]

    with open("./conf/application.conf", "r") as f:
        lines = f.readlines()
        config = tuple([line.strip().split("=")[1] for line in lines])
    database, username, password, host, port = config
    logger.info("Input configure data to success from application.conf")

    connection = psycopg2.connect(database=database, user=username, password=password, host=host, port=port)
    df = pd.read_sql(f"select * from {table_name}", connection)

    tracer = Tracer(span=options["span"], bandwidth=options["bandwidth"])
    if target is not None and target_mesh is not None:
        traceframe = df["owner" == target]
        pdf = tracer.fit(traceframe, "takendate", ref=traceframe["mesh_code" == target_mesh]).predict(traceframe, "takendate", mode="median")
        display.flow(pdf)
    elif target is not None:
        traceframe = df["owner" == target]
        pdf = tracer.fit(traceframe, "takendate").predict(traceframe, "takendate", mode="median")
        display.flow(pdf)
    elif target_mesh is not None:
        traceframe = df["mesh_code" == target_mesh]
        display.all(traceframe)
    else:
        target_mesh = input("Target mesh-code : ")
        traceframe = df["mesh_code" == target_mesh]
        display.all(traceframe)

    logger.info(f"Finished output to trace data on {df.shape[0]}")

    connection.close()

