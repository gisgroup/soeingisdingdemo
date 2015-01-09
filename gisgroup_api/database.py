"""
    gisgroup_api.database
    ~~~~~~~~~~~~~~~~~~~~~
    Provide database access
"""

import os
import psycopg2
import urllib

connection = psycopg2.connect(
    database="pgrouting",
    user="postgres",
    password="postgres",
    host="localhost",
    port=5432
)


def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import yourapplication.models
    Base.metadata.create_all(bind=engine)
