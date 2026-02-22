from alembic_utils.pg_function import PGFunction
from alembic_utils.pg_policy import PGPolicy


current_user_id = PGFunction(
    schema="public",
    signature="current_user_id()",
    definition=r"""
returns integer
language sql
stable
security definer
set search_path = public
as $$
  select u.id
  from public."user" u
  where u.auth_user_id = auth.uid()
$$;
""",
)

is_org_member = PGFunction(
    schema="public",
    signature="is_org_member(p_org_id integer)",
    definition=r"""
returns boolean
language sql
stable
security definer
set search_path = public
as $$
  select exists (
    select 1
    from public.user_group_association uga
    join public."group" g on g.id = uga.group_id
    where uga.user_id = public.current_user_id()
      and g.organisation_id = p_org_id
  );
$$;
""",
)

server_select_org_member = PGPolicy(
    schema="public",
    signature="server_select_org_member",  # policy name only
    on_entity="public.server",  # target table
    definition="""
        AS PERMISSIVE
        FOR SELECT
        TO authenticated
        USING (public.is_org_member(organisation_id))
    """,
)
