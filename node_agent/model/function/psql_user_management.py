from alembic_utils.pg_function import PGFunction


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

is_user = PGFunction(
    schema="public",
    signature="is_user()",
    definition=r"""
returns boolean
language sql
stable
security definer
set search_path = public
as $$
  select exists (
    select 1
    from public."user" u
    where u.auth_user_id = auth.uid()
  );
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

is_group_org_member = PGFunction(
    schema="public",
    signature="is_group_org_member(p_group_id integer)",
    definition=r"""
returns boolean
language sql
stable
security definer
set search_path = public
as $$
  select exists (
    select 1
    from public."group" g_target
    join public."group" g_member
      on g_member.organisation_id = g_target.organisation_id
    join public.user_group_association uga
      on uga.group_id = g_member.id
    where uga.user_id = public.current_user_id()
      and g_target.id = p_group_id
  );
$$;
""",
)

is_server_member = PGFunction(
    schema="public",
    signature="is_server_member(p_server_id integer)",
    definition=r"""
returns boolean
language sql
stable
security definer
set search_path = public
as $$
  select exists (
    select 1
    from public.server s
    join public.organisation o on o.id = s.organisation_id
    where s.id = p_server_id
      and public.is_org_member(o.id)
  );
$$;
""",
)
