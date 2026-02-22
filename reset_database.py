#!/usr/bin/3
from node_agent.model.db import db
from sqlalchemy import inspect, text

from node_agent.config import get_database_uri

db.init(get_database_uri())

inspector = inspect(db.engine)
schemas = inspector.get_schema_names()

for schema in schemas:
    if schema == "public":
        print("Dropping schema: %s" % schema)
        for table_name in inspector.get_table_names(schema=schema):
            print("Table: %s" % table_name)
            db.session.execute(
                text('DROP TABLE IF EXISTS "%s" CASCADE' % table_name)
            )
        functions = db.session.execute(
            text(
                """
                SELECT routine_name, routine_type
                FROM information_schema.routines
                WHERE specific_schema = :schema
            """
            ),
            {"schema": schema},
        ).fetchall()
        for func in functions:
            db.session.execute(
                text(f'DROP FUNCTION IF EXISTS "{func.routine_name}" CASCADE')
            )

        policies = db.session.execute(
            text(
                """
                SELECT policyname, tablename
                FROM pg_policies
                WHERE schemaname = :schema
            """
            ),
            {"schema": schema},
        ).fetchall()
        for policy in policies:
            db.session.execute(
                text(
                    f'DROP POLICY IF EXISTS "{policy.polname}" ON "{policy.tablename}" CASCADE'
                )
            )
    else:
        print("Skipping schema: %s" % schema)
db.session.commit()
