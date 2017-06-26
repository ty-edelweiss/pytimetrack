#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import psycopg2
import pandas as pd
import pandas.io.sql as psql

from pytimetrack.dataframe.track import Track

if __name__ == "__main__":
    with open("./test.json", "r") as f:
        test = json.load(f)

    connection = psycopg2.connect(database=test["database"], host="127.0.0.1", port=5432, user=test["user"], password=test["password"])

    test_table = test["table"]
    limitter = True
    sql = f"select * from {test_table}"
    sql = sql + " limit 100" if limitter else sql
    df = psql.read_sql(sql, connection)

    t = "takendate"
    track = Track(span=24.0, sequence=8.0).fit(df, t)
    pdf = track.predict(df, t)

    print(track.clusters_)

    print(pdf[[t, "labels"]])

    print(pdf["labels"].head())
