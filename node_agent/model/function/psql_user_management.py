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
      and g.organization_id = p_org_id
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
      on g_member.organization_id = g_target.organization_id
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
    join public.organization o on o.id = s.organization_id
    where s.id = p_server_id
      and public.is_org_member(o.id)
  );
$$;
""",
)

is_server_host_member = PGFunction(
    schema="public",
    signature="is_server_host_member(p_server_host_id integer)",
    definition=r"""
returns boolean
language sql
stable
security definer
set search_path = public
as $$
  select exists (
    select 1
    from public.server_host si
    join public.server s on s.id = si.server_id
    join public.organization o on o.id = s.organization_id
    where si.id = p_server_host_id
      and public.is_org_member(o.id)
  );
$$;
""",
)

is_server_port_member = PGFunction(
    schema="public",
    signature="is_server_port_member(p_server_port_id integer)",
    definition=r"""
returns boolean
language sql
stable
security definer
set search_path = public
as $$
  select exists (
    select 1
    from public.server_port sp
    join public.server_host si on si.id = sp.server_host_id
    join public.server s on s.id = si.server_id
    join public.organization o on o.id = s.organization_id
    where sp.id = p_server_port_id
      and public.is_org_member(o.id)
  );
$$;
""",
)
