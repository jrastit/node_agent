from alembic_utils.pg_function import PGFunction

list_public_tables = PGFunction(
    schema="public",
    signature="list_public_tables()",
    definition="""
returns table (
  table_name text
)
language sql
security definer
set search_path = public
as $$
  select tablename::text
  from pg_catalog.pg_tables
  where schemaname = 'public'
  order by tablename;
$$;
""",
)
