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
    "-l", "--level",
    choices=[4, 5, 6],
    default=4,
    help="level of mesh code",
    dest="level"
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
    default=180.0,
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

    table_name = VENDOR + "_mesh_" + str(options.level)

    with open("./conf/application.conf", "r") as f:
        lines = f.readlines()
        config = tuple([line.strip().split("=")[1] for line in lines if "=" in line])
    database, username, password, host, port = config
    logger.info("Input configure data to success from application.conf")

    connection = psycopg2.connect(database=database, user=username, password=password, host=host, port=port)

    tracer = Tracer(span=options.span, bandwidth=options.bandwidth)
    if options.target is not None and options.mesh is not None:
        traceframe = pd.read_sql(f"select * from {table_name} where owner like {options.target}")
        pdf = tracer.fit(traceframe, "takendate", ref=traceframe[traceframe["mesh_code"] == options.mesh]).predict(traceframe, "takendate", mode="median")
        display.flow(pdf)
    elif options.target is not None:
        traceframe = pd.read_sql(f"select * from {table_name} where owner like {options.target}", connection)
        pdf = tracer.fit(traceframe, "takendate").predict(traceframe, "takendate", mode="median")
        display.flow(pdf)
    elif options.mesh is not None:
        df = pd.read_sql(f"select * from {table_name} where mesh_code = {options.mesh}", connection)
        display.all(df)
    else:
        options.mesh = int(input("target mesh-code : "))
        df = pd.read_sql(f"select * from {table_name} where mesh_code = {options.mesh}", connection)
        display.all(df)

    logger.info(f"Finished output to trace data on {df.shape[0]}")

    connection.close()

