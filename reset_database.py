#!/usr/bin/3
import os
from flask import Flask

from node_agent.model.db import db
from sqlalchemy import inspect, text

from node_agent.config import get_database_uri

# Create the web app
app = Flask(__name__)
# configure the Postgres database
app.config["SQLALCHEMY_DATABASE_URI"] = get_database_uri()
# initialize the app with the extension

db.init_app(app)

with app.app_context():
    inspector = inspect(db.engine)
    schemas = inspector.get_schema_names()

    for schema in schemas:
        if schema == "public":
            print("Dropping schema: %s" % schema)
            for table_name in inspector.get_table_names(schema=schema):
                print("Table: %s" % table_name)
                # for column in inspector.get_columns(table_name, schema=schema):
                #    print("Column: %s" % column)
                db.session.execute(
                    text("DROP TABLE IF EXISTS %s CASCADE" % table_name)
                )
        else:
            print("Skipping schema: %s" % schema)
    db.session.commit()
