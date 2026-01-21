Loading settings from /home/oasis/node_agent/settings/settings.yaml and /home/oasis/node_agent/settings/.secrets.yaml
METADATA TABLES: ['entrypoint', 'group', 'oasis_config', 'oasis_entity', 'oasis_network', 'oasis_node', 'oasis_node_nodetype', 'oasis_nodetype', 'oasis_paratime_config', 'organisation', 'server', 'user', 'user_group_association']
BEGIN;

CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL, 
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

-- Running upgrade  -> 20260121_01_rls

CREATE TABLE oasis_config (
    id SERIAL NOT NULL, 
    time_create TIMESTAMP WITHOUT TIME ZONE DEFAULT now() NOT NULL, 
    time_updated TIMESTAMP WITHOUT TIME ZONE DEFAULT now() NOT NULL, 
    md5 VARCHAR, 
    network VARCHAR, 
    network_genesis_file VARCHAR, 
    network_seed_node VARCHAR, 
    network_core_version VARCHAR, 
    network_core_version_url VARCHAR, 
    validate BOOLEAN, 
    PRIMARY KEY (id)
);

CREATE TABLE oasis_entity (
    id SERIAL NOT NULL, 
    time_create TIMESTAMP WITHOUT TIME ZONE DEFAULT now() NOT NULL, 
    time_updated TIMESTAMP WITHOUT TIME ZONE DEFAULT now() NOT NULL, 
    name VARCHAR NOT NULL, 
    entity_id VARCHAR, 
    PRIMARY KEY (id)
);

CREATE TABLE oasis_network (
    id SERIAL NOT NULL, 
    time_create TIMESTAMP WITHOUT TIME ZONE DEFAULT now() NOT NULL, 
    time_updated TIMESTAMP WITHOUT TIME ZONE DEFAULT now() NOT NULL, 
    name VARCHAR NOT NULL, 
    core_version VARCHAR, 
    genesis_url VARCHAR, 
    seed_node VARCHAR, 
    PRIMARY KEY (id)
);

CREATE TABLE organisation (
    id SERIAL NOT NULL, 
    time_create TIMESTAMP WITHOUT TIME ZONE DEFAULT now() NOT NULL, 
    time_updated TIMESTAMP WITHOUT TIME ZONE DEFAULT now() NOT NULL, 
    name VARCHAR NOT NULL, 
    parent_id INTEGER, 
    PRIMARY KEY (id), 
    FOREIGN KEY(parent_id) REFERENCES organisation (id)
);

CREATE TABLE "user" (
    id SERIAL NOT NULL, 
    auth_user_id UUID, 
    time_create TIMESTAMP WITHOUT TIME ZONE DEFAULT now() NOT NULL, 
    time_updated TIMESTAMP WITHOUT TIME ZONE DEFAULT now() NOT NULL, 
    PRIMARY KEY (id), 
    UNIQUE (auth_user_id)
);

CREATE TABLE "group" (
    id SERIAL NOT NULL, 
    time_create TIMESTAMP WITHOUT TIME ZONE DEFAULT now() NOT NULL, 
    time_updated TIMESTAMP WITHOUT TIME ZONE DEFAULT now() NOT NULL, 
    name VARCHAR NOT NULL, 
    organisation_id INTEGER, 
    PRIMARY KEY (id), 
    FOREIGN KEY(organisation_id) REFERENCES organisation (id)
);

CREATE TABLE oasis_nodetype (
    id SERIAL NOT NULL, 
    time_create TIMESTAMP WITHOUT TIME ZONE DEFAULT now() NOT NULL, 
    time_updated TIMESTAMP WITHOUT TIME ZONE DEFAULT now() NOT NULL, 
    name VARCHAR NOT NULL, 
    core_version VARCHAR, 
    runtime_identifier VARCHAR, 
    runtime_version VARCHAR, 
    runtime_version_old VARCHAR, 
    runtime_ias VARCHAR, 
    latest_time_error VARCHAR, 
    paratime_worker_client_port VARCHAR, 
    paratime_worker_p2p_port VARCHAR, 
    node_ssh_id VARCHAR, 
    network_id INTEGER, 
    PRIMARY KEY (id), 
    FOREIGN KEY(network_id) REFERENCES oasis_network (id)
);

CREATE TABLE oasis_paratime_config (
    id SERIAL NOT NULL, 
    time_create TIMESTAMP WITHOUT TIME ZONE DEFAULT now() NOT NULL, 
    time_updated TIMESTAMP WITHOUT TIME ZONE DEFAULT now() NOT NULL, 
    name VARCHAR NOT NULL, 
    core_version VARCHAR, 
    core_version_url VARCHAR, 
    runtime_identifier VARCHAR, 
    runtime_version VARCHAR, 
    runtime_version_url VARCHAR, 
    "IAS_proxy" VARCHAR, 
    oasis_config_id INTEGER, 
    PRIMARY KEY (id), 
    FOREIGN KEY(oasis_config_id) REFERENCES oasis_config (id)
);

CREATE TABLE server (
    id SERIAL NOT NULL, 
    time_create TIMESTAMP WITHOUT TIME ZONE DEFAULT now() NOT NULL, 
    time_updated TIMESTAMP WITHOUT TIME ZONE DEFAULT now() NOT NULL, 
    name VARCHAR NOT NULL, 
    cloud VARCHAR, 
    cloud_name VARCHAR, 
    ip VARCHAR, 
    organisation_id INTEGER, 
    PRIMARY KEY (id), 
    FOREIGN KEY(organisation_id) REFERENCES organisation (id)
);

CREATE TABLE entrypoint (
    id SERIAL NOT NULL, 
    time_create TIMESTAMP WITHOUT TIME ZONE DEFAULT now() NOT NULL, 
    time_updated TIMESTAMP WITHOUT TIME ZONE DEFAULT now() NOT NULL, 
    name VARCHAR, 
    "user" VARCHAR, 
    path VARCHAR, 
    ssh_id VARCHAR, 
    server_id INTEGER, 
    PRIMARY KEY (id), 
    FOREIGN KEY(server_id) REFERENCES server (id) ON DELETE CASCADE
);

CREATE TABLE user_group_association (
    user_id INTEGER NOT NULL, 
    group_id INTEGER NOT NULL, 
    PRIMARY KEY (user_id, group_id), 
    FOREIGN KEY(group_id) REFERENCES "group" (id), 
    FOREIGN KEY(user_id) REFERENCES "user" (id)
);

CREATE TABLE oasis_node (
    id SERIAL NOT NULL, 
    time_create TIMESTAMP WITHOUT TIME ZONE DEFAULT now() NOT NULL, 
    time_updated TIMESTAMP WITHOUT TIME ZONE DEFAULT now() NOT NULL, 
    name VARCHAR NOT NULL, 
    core_version VARCHAR, 
    genesis_url VARCHAR, 
    seed_node VARCHAR, 
    node_root_dir VARCHAR, 
    node_address VARCHAR, 
    node_port VARCHAR, 
    paratime_worker_client_port VARCHAR, 
    paratime_worker_p2p_port VARCHAR, 
    node_id VARCHAR, 
    entity_id INTEGER, 
    entrypoint_id INTEGER, 
    entrypoint_admin_id INTEGER, 
    PRIMARY KEY (id), 
    FOREIGN KEY(entity_id) REFERENCES oasis_entity (id), 
    FOREIGN KEY(entrypoint_admin_id) REFERENCES entrypoint (id) ON DELETE SET NULL, 
    FOREIGN KEY(entrypoint_id) REFERENCES entrypoint (id) ON DELETE SET NULL
);

CREATE TABLE oasis_node_nodetype (
    node_id INTEGER NOT NULL, 
    nodetype_id INTEGER NOT NULL, 
    PRIMARY KEY (node_id, nodetype_id), 
    FOREIGN KEY(node_id) REFERENCES oasis_node (id), 
    FOREIGN KEY(nodetype_id) REFERENCES oasis_nodetype (id)
);

INSERT INTO alembic_version (version_num) VALUES ('20260121_01_rls') RETURNING alembic_version.version_num;

-- Running upgrade 20260121_01_rls -> 20260121_02_rls

CREATE FUNCTION "public"."current_user_id"() returns integer
language sql
stable
security definer
set search_path = public
as $$
  select u.id
  from public.user u
  where u.auth_user_id = auth.uid()
$$;

CREATE FUNCTION "public"."is_org_member"(p_org_id integer) returns boolean
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

REVOKE INSERT ON "public"."alembic_version" FROM "anon";

REVOKE REFERENCES ON "public"."alembic_version" FROM "anon";

REVOKE SELECT ON "public"."alembic_version" FROM "anon";

REVOKE UPDATE ON "public"."alembic_version" FROM "anon";

REVOKE INSERT ON "public"."alembic_version" FROM "authenticated";

REVOKE REFERENCES ON "public"."alembic_version" FROM "authenticated";

REVOKE SELECT ON "public"."alembic_version" FROM "authenticated";

REVOKE UPDATE ON "public"."alembic_version" FROM "authenticated";

REVOKE INSERT ON "public"."alembic_version" FROM "postgres";

REVOKE REFERENCES ON "public"."alembic_version" FROM "postgres";

REVOKE SELECT ON "public"."alembic_version" FROM "postgres";

REVOKE UPDATE ON "public"."alembic_version" FROM "postgres";

REVOKE INSERT ON "public"."alembic_version" FROM "service_role";

REVOKE REFERENCES ON "public"."alembic_version" FROM "service_role";

REVOKE SELECT ON "public"."alembic_version" FROM "service_role";

REVOKE UPDATE ON "public"."alembic_version" FROM "service_role";

REVOKE INSERT ON "public"."entrypoint" FROM "anon";

REVOKE REFERENCES ON "public"."entrypoint" FROM "anon";

REVOKE SELECT ON "public"."entrypoint" FROM "anon";

REVOKE UPDATE ON "public"."entrypoint" FROM "anon";

REVOKE INSERT ON "public"."entrypoint" FROM "authenticated";

REVOKE REFERENCES ON "public"."entrypoint" FROM "authenticated";

REVOKE SELECT ON "public"."entrypoint" FROM "authenticated";

REVOKE UPDATE ON "public"."entrypoint" FROM "authenticated";

REVOKE INSERT ON "public"."entrypoint" FROM "postgres";

REVOKE REFERENCES ON "public"."entrypoint" FROM "postgres";

REVOKE SELECT ON "public"."entrypoint" FROM "postgres";

REVOKE UPDATE ON "public"."entrypoint" FROM "postgres";

REVOKE INSERT ON "public"."entrypoint" FROM "service_role";

REVOKE REFERENCES ON "public"."entrypoint" FROM "service_role";

REVOKE SELECT ON "public"."entrypoint" FROM "service_role";

REVOKE UPDATE ON "public"."entrypoint" FROM "service_role";

REVOKE INSERT ON "public"."group" FROM "anon";

REVOKE REFERENCES ON "public"."group" FROM "anon";

REVOKE SELECT ON "public"."group" FROM "anon";

REVOKE UPDATE ON "public"."group" FROM "anon";

REVOKE INSERT ON "public"."group" FROM "authenticated";

REVOKE REFERENCES ON "public"."group" FROM "authenticated";

REVOKE SELECT ON "public"."group" FROM "authenticated";

REVOKE UPDATE ON "public"."group" FROM "authenticated";

REVOKE INSERT ON "public"."group" FROM "postgres";

REVOKE REFERENCES ON "public"."group" FROM "postgres";

REVOKE SELECT ON "public"."group" FROM "postgres";

REVOKE UPDATE ON "public"."group" FROM "postgres";

REVOKE INSERT ON "public"."group" FROM "service_role";

REVOKE REFERENCES ON "public"."group" FROM "service_role";

REVOKE SELECT ON "public"."group" FROM "service_role";

REVOKE UPDATE ON "public"."group" FROM "service_role";

REVOKE INSERT ON "public"."oasis_config" FROM "anon";

REVOKE REFERENCES ON "public"."oasis_config" FROM "anon";

REVOKE SELECT ON "public"."oasis_config" FROM "anon";

REVOKE UPDATE ON "public"."oasis_config" FROM "anon";

REVOKE INSERT ON "public"."oasis_config" FROM "authenticated";

REVOKE REFERENCES ON "public"."oasis_config" FROM "authenticated";

REVOKE SELECT ON "public"."oasis_config" FROM "authenticated";

REVOKE UPDATE ON "public"."oasis_config" FROM "authenticated";

REVOKE INSERT ON "public"."oasis_config" FROM "postgres";

REVOKE REFERENCES ON "public"."oasis_config" FROM "postgres";

REVOKE SELECT ON "public"."oasis_config" FROM "postgres";

REVOKE UPDATE ON "public"."oasis_config" FROM "postgres";

REVOKE INSERT ON "public"."oasis_config" FROM "service_role";

REVOKE REFERENCES ON "public"."oasis_config" FROM "service_role";

REVOKE SELECT ON "public"."oasis_config" FROM "service_role";

REVOKE UPDATE ON "public"."oasis_config" FROM "service_role";

REVOKE INSERT ON "public"."oasis_entity" FROM "anon";

REVOKE REFERENCES ON "public"."oasis_entity" FROM "anon";

REVOKE SELECT ON "public"."oasis_entity" FROM "anon";

REVOKE UPDATE ON "public"."oasis_entity" FROM "anon";

REVOKE INSERT ON "public"."oasis_entity" FROM "authenticated";

REVOKE REFERENCES ON "public"."oasis_entity" FROM "authenticated";

REVOKE SELECT ON "public"."oasis_entity" FROM "authenticated";

REVOKE UPDATE ON "public"."oasis_entity" FROM "authenticated";

REVOKE INSERT ON "public"."oasis_entity" FROM "postgres";

REVOKE REFERENCES ON "public"."oasis_entity" FROM "postgres";

REVOKE SELECT ON "public"."oasis_entity" FROM "postgres";

REVOKE UPDATE ON "public"."oasis_entity" FROM "postgres";

REVOKE INSERT ON "public"."oasis_entity" FROM "service_role";

REVOKE REFERENCES ON "public"."oasis_entity" FROM "service_role";

REVOKE SELECT ON "public"."oasis_entity" FROM "service_role";

REVOKE UPDATE ON "public"."oasis_entity" FROM "service_role";

REVOKE INSERT ON "public"."oasis_network" FROM "anon";

REVOKE REFERENCES ON "public"."oasis_network" FROM "anon";

REVOKE SELECT ON "public"."oasis_network" FROM "anon";

REVOKE UPDATE ON "public"."oasis_network" FROM "anon";

REVOKE INSERT ON "public"."oasis_network" FROM "authenticated";

REVOKE REFERENCES ON "public"."oasis_network" FROM "authenticated";

REVOKE SELECT ON "public"."oasis_network" FROM "authenticated";

REVOKE UPDATE ON "public"."oasis_network" FROM "authenticated";

REVOKE INSERT ON "public"."oasis_network" FROM "postgres";

REVOKE REFERENCES ON "public"."oasis_network" FROM "postgres";

REVOKE SELECT ON "public"."oasis_network" FROM "postgres";

REVOKE UPDATE ON "public"."oasis_network" FROM "postgres";

REVOKE INSERT ON "public"."oasis_network" FROM "service_role";

REVOKE REFERENCES ON "public"."oasis_network" FROM "service_role";

REVOKE SELECT ON "public"."oasis_network" FROM "service_role";

REVOKE UPDATE ON "public"."oasis_network" FROM "service_role";

REVOKE INSERT ON "public"."oasis_node" FROM "anon";

REVOKE REFERENCES ON "public"."oasis_node" FROM "anon";

REVOKE SELECT ON "public"."oasis_node" FROM "anon";

REVOKE UPDATE ON "public"."oasis_node" FROM "anon";

REVOKE INSERT ON "public"."oasis_node" FROM "authenticated";

REVOKE REFERENCES ON "public"."oasis_node" FROM "authenticated";

REVOKE SELECT ON "public"."oasis_node" FROM "authenticated";

REVOKE UPDATE ON "public"."oasis_node" FROM "authenticated";

REVOKE INSERT ON "public"."oasis_node" FROM "postgres";

REVOKE REFERENCES ON "public"."oasis_node" FROM "postgres";

REVOKE SELECT ON "public"."oasis_node" FROM "postgres";

REVOKE UPDATE ON "public"."oasis_node" FROM "postgres";

REVOKE INSERT ON "public"."oasis_node" FROM "service_role";

REVOKE REFERENCES ON "public"."oasis_node" FROM "service_role";

REVOKE SELECT ON "public"."oasis_node" FROM "service_role";

REVOKE UPDATE ON "public"."oasis_node" FROM "service_role";

REVOKE INSERT ON "public"."oasis_node_nodetype" FROM "anon";

REVOKE REFERENCES ON "public"."oasis_node_nodetype" FROM "anon";

REVOKE SELECT ON "public"."oasis_node_nodetype" FROM "anon";

REVOKE UPDATE ON "public"."oasis_node_nodetype" FROM "anon";

REVOKE INSERT ON "public"."oasis_node_nodetype" FROM "authenticated";

REVOKE REFERENCES ON "public"."oasis_node_nodetype" FROM "authenticated";

REVOKE SELECT ON "public"."oasis_node_nodetype" FROM "authenticated";

REVOKE UPDATE ON "public"."oasis_node_nodetype" FROM "authenticated";

REVOKE INSERT ON "public"."oasis_node_nodetype" FROM "postgres";

REVOKE REFERENCES ON "public"."oasis_node_nodetype" FROM "postgres";

REVOKE SELECT ON "public"."oasis_node_nodetype" FROM "postgres";

REVOKE UPDATE ON "public"."oasis_node_nodetype" FROM "postgres";

REVOKE INSERT ON "public"."oasis_node_nodetype" FROM "service_role";

REVOKE REFERENCES ON "public"."oasis_node_nodetype" FROM "service_role";

REVOKE SELECT ON "public"."oasis_node_nodetype" FROM "service_role";

REVOKE UPDATE ON "public"."oasis_node_nodetype" FROM "service_role";

REVOKE INSERT ON "public"."oasis_nodetype" FROM "anon";

REVOKE REFERENCES ON "public"."oasis_nodetype" FROM "anon";

REVOKE SELECT ON "public"."oasis_nodetype" FROM "anon";

REVOKE UPDATE ON "public"."oasis_nodetype" FROM "anon";

REVOKE INSERT ON "public"."oasis_nodetype" FROM "authenticated";

REVOKE REFERENCES ON "public"."oasis_nodetype" FROM "authenticated";

REVOKE SELECT ON "public"."oasis_nodetype" FROM "authenticated";

REVOKE UPDATE ON "public"."oasis_nodetype" FROM "authenticated";

REVOKE INSERT ON "public"."oasis_nodetype" FROM "postgres";

REVOKE REFERENCES ON "public"."oasis_nodetype" FROM "postgres";

REVOKE SELECT ON "public"."oasis_nodetype" FROM "postgres";

REVOKE UPDATE ON "public"."oasis_nodetype" FROM "postgres";

REVOKE INSERT ON "public"."oasis_nodetype" FROM "service_role";

REVOKE REFERENCES ON "public"."oasis_nodetype" FROM "service_role";

REVOKE SELECT ON "public"."oasis_nodetype" FROM "service_role";

REVOKE UPDATE ON "public"."oasis_nodetype" FROM "service_role";

REVOKE INSERT ON "public"."oasis_paratime_config" FROM "anon";

REVOKE REFERENCES ON "public"."oasis_paratime_config" FROM "anon";

REVOKE SELECT ON "public"."oasis_paratime_config" FROM "anon";

REVOKE UPDATE ON "public"."oasis_paratime_config" FROM "anon";

REVOKE INSERT ON "public"."oasis_paratime_config" FROM "authenticated";

REVOKE REFERENCES ON "public"."oasis_paratime_config" FROM "authenticated";

REVOKE SELECT ON "public"."oasis_paratime_config" FROM "authenticated";

REVOKE UPDATE ON "public"."oasis_paratime_config" FROM "authenticated";

REVOKE INSERT ON "public"."oasis_paratime_config" FROM "postgres";

REVOKE REFERENCES ON "public"."oasis_paratime_config" FROM "postgres";

REVOKE SELECT ON "public"."oasis_paratime_config" FROM "postgres";

REVOKE UPDATE ON "public"."oasis_paratime_config" FROM "postgres";

REVOKE INSERT ON "public"."oasis_paratime_config" FROM "service_role";

REVOKE REFERENCES ON "public"."oasis_paratime_config" FROM "service_role";

REVOKE SELECT ON "public"."oasis_paratime_config" FROM "service_role";

REVOKE UPDATE ON "public"."oasis_paratime_config" FROM "service_role";

REVOKE INSERT ON "public"."organisation" FROM "anon";

REVOKE REFERENCES ON "public"."organisation" FROM "anon";

REVOKE SELECT ON "public"."organisation" FROM "anon";

REVOKE UPDATE ON "public"."organisation" FROM "anon";

REVOKE INSERT ON "public"."organisation" FROM "authenticated";

REVOKE REFERENCES ON "public"."organisation" FROM "authenticated";

REVOKE SELECT ON "public"."organisation" FROM "authenticated";

REVOKE UPDATE ON "public"."organisation" FROM "authenticated";

REVOKE INSERT ON "public"."organisation" FROM "postgres";

REVOKE REFERENCES ON "public"."organisation" FROM "postgres";

REVOKE SELECT ON "public"."organisation" FROM "postgres";

REVOKE UPDATE ON "public"."organisation" FROM "postgres";

REVOKE INSERT ON "public"."organisation" FROM "service_role";

REVOKE REFERENCES ON "public"."organisation" FROM "service_role";

REVOKE SELECT ON "public"."organisation" FROM "service_role";

REVOKE UPDATE ON "public"."organisation" FROM "service_role";

REVOKE INSERT ON "public"."server" FROM "anon";

REVOKE REFERENCES ON "public"."server" FROM "anon";

REVOKE SELECT ON "public"."server" FROM "anon";

REVOKE UPDATE ON "public"."server" FROM "anon";

REVOKE INSERT ON "public"."server" FROM "authenticated";

REVOKE REFERENCES ON "public"."server" FROM "authenticated";

REVOKE SELECT ON "public"."server" FROM "authenticated";

REVOKE UPDATE ON "public"."server" FROM "authenticated";

REVOKE INSERT ON "public"."server" FROM "postgres";

REVOKE REFERENCES ON "public"."server" FROM "postgres";

REVOKE SELECT ON "public"."server" FROM "postgres";

REVOKE UPDATE ON "public"."server" FROM "postgres";

REVOKE INSERT ON "public"."server" FROM "service_role";

REVOKE REFERENCES ON "public"."server" FROM "service_role";

REVOKE SELECT ON "public"."server" FROM "service_role";

REVOKE UPDATE ON "public"."server" FROM "service_role";

REVOKE INSERT ON "public"."user" FROM "anon";

REVOKE REFERENCES ON "public"."user" FROM "anon";

REVOKE SELECT ON "public"."user" FROM "anon";

REVOKE UPDATE ON "public"."user" FROM "anon";

REVOKE INSERT ON "public"."user" FROM "authenticated";

REVOKE REFERENCES ON "public"."user" FROM "authenticated";

REVOKE SELECT ON "public"."user" FROM "authenticated";

REVOKE UPDATE ON "public"."user" FROM "authenticated";

REVOKE INSERT ON "public"."user" FROM "postgres";

REVOKE REFERENCES ON "public"."user" FROM "postgres";

REVOKE SELECT ON "public"."user" FROM "postgres";

REVOKE UPDATE ON "public"."user" FROM "postgres";

REVOKE INSERT ON "public"."user" FROM "service_role";

REVOKE REFERENCES ON "public"."user" FROM "service_role";

REVOKE SELECT ON "public"."user" FROM "service_role";

REVOKE UPDATE ON "public"."user" FROM "service_role";

REVOKE INSERT ON "public"."user_group_association" FROM "anon";

REVOKE REFERENCES ON "public"."user_group_association" FROM "anon";

REVOKE SELECT ON "public"."user_group_association" FROM "anon";

REVOKE UPDATE ON "public"."user_group_association" FROM "anon";

REVOKE INSERT ON "public"."user_group_association" FROM "authenticated";

REVOKE REFERENCES ON "public"."user_group_association" FROM "authenticated";

REVOKE SELECT ON "public"."user_group_association" FROM "authenticated";

REVOKE UPDATE ON "public"."user_group_association" FROM "authenticated";

REVOKE INSERT ON "public"."user_group_association" FROM "postgres";

REVOKE REFERENCES ON "public"."user_group_association" FROM "postgres";

REVOKE SELECT ON "public"."user_group_association" FROM "postgres";

REVOKE UPDATE ON "public"."user_group_association" FROM "postgres";

REVOKE INSERT ON "public"."user_group_association" FROM "service_role";

REVOKE REFERENCES ON "public"."user_group_association" FROM "service_role";

REVOKE SELECT ON "public"."user_group_association" FROM "service_role";

REVOKE UPDATE ON "public"."user_group_association" FROM "service_role";

REVOKE DELETE ON "public"."alembic_version" FROM "postgres";

REVOKE TRUNCATE ON "public"."alembic_version" FROM "postgres";

REVOKE TRIGGER ON "public"."alembic_version" FROM "postgres";

REVOKE DELETE ON "public"."alembic_version" FROM "anon";

REVOKE TRUNCATE ON "public"."alembic_version" FROM "anon";

REVOKE TRIGGER ON "public"."alembic_version" FROM "anon";

REVOKE DELETE ON "public"."alembic_version" FROM "authenticated";

REVOKE TRUNCATE ON "public"."alembic_version" FROM "authenticated";

REVOKE TRIGGER ON "public"."alembic_version" FROM "authenticated";

REVOKE DELETE ON "public"."alembic_version" FROM "service_role";

REVOKE TRUNCATE ON "public"."alembic_version" FROM "service_role";

REVOKE TRIGGER ON "public"."alembic_version" FROM "service_role";

REVOKE DELETE ON "public"."organisation" FROM "postgres";

REVOKE TRUNCATE ON "public"."organisation" FROM "postgres";

REVOKE TRIGGER ON "public"."organisation" FROM "postgres";

REVOKE DELETE ON "public"."organisation" FROM "anon";

REVOKE TRUNCATE ON "public"."organisation" FROM "anon";

REVOKE TRIGGER ON "public"."organisation" FROM "anon";

REVOKE DELETE ON "public"."organisation" FROM "authenticated";

REVOKE TRUNCATE ON "public"."organisation" FROM "authenticated";

REVOKE TRIGGER ON "public"."organisation" FROM "authenticated";

REVOKE DELETE ON "public"."organisation" FROM "service_role";

REVOKE TRUNCATE ON "public"."organisation" FROM "service_role";

REVOKE TRIGGER ON "public"."organisation" FROM "service_role";

REVOKE DELETE ON "public"."group" FROM "postgres";

REVOKE TRUNCATE ON "public"."group" FROM "postgres";

REVOKE TRIGGER ON "public"."group" FROM "postgres";

REVOKE DELETE ON "public"."group" FROM "anon";

REVOKE TRUNCATE ON "public"."group" FROM "anon";

REVOKE TRIGGER ON "public"."group" FROM "anon";

REVOKE DELETE ON "public"."group" FROM "authenticated";

REVOKE TRUNCATE ON "public"."group" FROM "authenticated";

REVOKE TRIGGER ON "public"."group" FROM "authenticated";

REVOKE DELETE ON "public"."group" FROM "service_role";

REVOKE TRUNCATE ON "public"."group" FROM "service_role";

REVOKE TRIGGER ON "public"."group" FROM "service_role";

REVOKE DELETE ON "public"."oasis_network" FROM "postgres";

REVOKE TRUNCATE ON "public"."oasis_network" FROM "postgres";

REVOKE TRIGGER ON "public"."oasis_network" FROM "postgres";

REVOKE DELETE ON "public"."oasis_network" FROM "anon";

REVOKE TRUNCATE ON "public"."oasis_network" FROM "anon";

REVOKE TRIGGER ON "public"."oasis_network" FROM "anon";

REVOKE DELETE ON "public"."oasis_network" FROM "authenticated";

REVOKE TRUNCATE ON "public"."oasis_network" FROM "authenticated";

REVOKE TRIGGER ON "public"."oasis_network" FROM "authenticated";

REVOKE DELETE ON "public"."oasis_network" FROM "service_role";

REVOKE TRUNCATE ON "public"."oasis_network" FROM "service_role";

REVOKE TRIGGER ON "public"."oasis_network" FROM "service_role";

REVOKE DELETE ON "public"."oasis_nodetype" FROM "postgres";

REVOKE TRUNCATE ON "public"."oasis_nodetype" FROM "postgres";

REVOKE TRIGGER ON "public"."oasis_nodetype" FROM "postgres";

REVOKE DELETE ON "public"."oasis_nodetype" FROM "anon";

REVOKE TRUNCATE ON "public"."oasis_nodetype" FROM "anon";

REVOKE TRIGGER ON "public"."oasis_nodetype" FROM "anon";

REVOKE DELETE ON "public"."oasis_nodetype" FROM "authenticated";

REVOKE TRUNCATE ON "public"."oasis_nodetype" FROM "authenticated";

REVOKE TRIGGER ON "public"."oasis_nodetype" FROM "authenticated";

REVOKE DELETE ON "public"."oasis_nodetype" FROM "service_role";

REVOKE TRUNCATE ON "public"."oasis_nodetype" FROM "service_role";

REVOKE TRIGGER ON "public"."oasis_nodetype" FROM "service_role";

REVOKE DELETE ON "public"."oasis_config" FROM "postgres";

REVOKE TRUNCATE ON "public"."oasis_config" FROM "postgres";

REVOKE TRIGGER ON "public"."oasis_config" FROM "postgres";

REVOKE DELETE ON "public"."oasis_config" FROM "anon";

REVOKE TRUNCATE ON "public"."oasis_config" FROM "anon";

REVOKE TRIGGER ON "public"."oasis_config" FROM "anon";

REVOKE DELETE ON "public"."oasis_config" FROM "authenticated";

REVOKE TRUNCATE ON "public"."oasis_config" FROM "authenticated";

REVOKE TRIGGER ON "public"."oasis_config" FROM "authenticated";

REVOKE DELETE ON "public"."oasis_config" FROM "service_role";

REVOKE TRUNCATE ON "public"."oasis_config" FROM "service_role";

REVOKE TRIGGER ON "public"."oasis_config" FROM "service_role";

REVOKE DELETE ON "public"."oasis_paratime_config" FROM "postgres";

REVOKE TRUNCATE ON "public"."oasis_paratime_config" FROM "postgres";

REVOKE TRIGGER ON "public"."oasis_paratime_config" FROM "postgres";

REVOKE DELETE ON "public"."oasis_paratime_config" FROM "anon";

REVOKE TRUNCATE ON "public"."oasis_paratime_config" FROM "anon";

REVOKE TRIGGER ON "public"."oasis_paratime_config" FROM "anon";

REVOKE DELETE ON "public"."oasis_paratime_config" FROM "authenticated";

REVOKE TRUNCATE ON "public"."oasis_paratime_config" FROM "authenticated";

REVOKE TRIGGER ON "public"."oasis_paratime_config" FROM "authenticated";

REVOKE DELETE ON "public"."oasis_paratime_config" FROM "service_role";

REVOKE TRUNCATE ON "public"."oasis_paratime_config" FROM "service_role";

REVOKE TRIGGER ON "public"."oasis_paratime_config" FROM "service_role";

REVOKE DELETE ON "public"."server" FROM "postgres";

REVOKE TRUNCATE ON "public"."server" FROM "postgres";

REVOKE TRIGGER ON "public"."server" FROM "postgres";

REVOKE DELETE ON "public"."server" FROM "anon";

REVOKE TRUNCATE ON "public"."server" FROM "anon";

REVOKE TRIGGER ON "public"."server" FROM "anon";

REVOKE DELETE ON "public"."server" FROM "authenticated";

REVOKE TRUNCATE ON "public"."server" FROM "authenticated";

REVOKE TRIGGER ON "public"."server" FROM "authenticated";

REVOKE DELETE ON "public"."server" FROM "service_role";

REVOKE TRUNCATE ON "public"."server" FROM "service_role";

REVOKE TRIGGER ON "public"."server" FROM "service_role";

REVOKE DELETE ON "public"."entrypoint" FROM "postgres";

REVOKE TRUNCATE ON "public"."entrypoint" FROM "postgres";

REVOKE TRIGGER ON "public"."entrypoint" FROM "postgres";

REVOKE DELETE ON "public"."entrypoint" FROM "anon";

REVOKE TRUNCATE ON "public"."entrypoint" FROM "anon";

REVOKE TRIGGER ON "public"."entrypoint" FROM "anon";

REVOKE DELETE ON "public"."entrypoint" FROM "authenticated";

REVOKE TRUNCATE ON "public"."entrypoint" FROM "authenticated";

REVOKE TRIGGER ON "public"."entrypoint" FROM "authenticated";

REVOKE DELETE ON "public"."entrypoint" FROM "service_role";

REVOKE TRUNCATE ON "public"."entrypoint" FROM "service_role";

REVOKE TRIGGER ON "public"."entrypoint" FROM "service_role";

REVOKE DELETE ON "public"."user_group_association" FROM "postgres";

REVOKE TRUNCATE ON "public"."user_group_association" FROM "postgres";

REVOKE TRIGGER ON "public"."user_group_association" FROM "postgres";

REVOKE DELETE ON "public"."user_group_association" FROM "anon";

REVOKE TRUNCATE ON "public"."user_group_association" FROM "anon";

REVOKE TRIGGER ON "public"."user_group_association" FROM "anon";

REVOKE DELETE ON "public"."user_group_association" FROM "authenticated";

REVOKE TRUNCATE ON "public"."user_group_association" FROM "authenticated";

REVOKE TRIGGER ON "public"."user_group_association" FROM "authenticated";

REVOKE DELETE ON "public"."user_group_association" FROM "service_role";

REVOKE TRUNCATE ON "public"."user_group_association" FROM "service_role";

REVOKE TRIGGER ON "public"."user_group_association" FROM "service_role";

REVOKE DELETE ON "public"."user" FROM "postgres";

REVOKE TRUNCATE ON "public"."user" FROM "postgres";

REVOKE TRIGGER ON "public"."user" FROM "postgres";

REVOKE DELETE ON "public"."user" FROM "anon";

REVOKE TRUNCATE ON "public"."user" FROM "anon";

REVOKE TRIGGER ON "public"."user" FROM "anon";

REVOKE DELETE ON "public"."user" FROM "authenticated";

REVOKE TRUNCATE ON "public"."user" FROM "authenticated";

REVOKE TRIGGER ON "public"."user" FROM "authenticated";

REVOKE DELETE ON "public"."user" FROM "service_role";

REVOKE TRUNCATE ON "public"."user" FROM "service_role";

REVOKE TRIGGER ON "public"."user" FROM "service_role";

REVOKE DELETE ON "public"."oasis_entity" FROM "postgres";

REVOKE TRUNCATE ON "public"."oasis_entity" FROM "postgres";

REVOKE TRIGGER ON "public"."oasis_entity" FROM "postgres";

REVOKE DELETE ON "public"."oasis_entity" FROM "anon";

REVOKE TRUNCATE ON "public"."oasis_entity" FROM "anon";

REVOKE TRIGGER ON "public"."oasis_entity" FROM "anon";

REVOKE DELETE ON "public"."oasis_entity" FROM "authenticated";

REVOKE TRUNCATE ON "public"."oasis_entity" FROM "authenticated";

REVOKE TRIGGER ON "public"."oasis_entity" FROM "authenticated";

REVOKE DELETE ON "public"."oasis_entity" FROM "service_role";

REVOKE TRUNCATE ON "public"."oasis_entity" FROM "service_role";

REVOKE TRIGGER ON "public"."oasis_entity" FROM "service_role";

REVOKE DELETE ON "public"."oasis_node" FROM "postgres";

REVOKE TRUNCATE ON "public"."oasis_node" FROM "postgres";

REVOKE TRIGGER ON "public"."oasis_node" FROM "postgres";

REVOKE DELETE ON "public"."oasis_node" FROM "anon";

REVOKE TRUNCATE ON "public"."oasis_node" FROM "anon";

REVOKE TRIGGER ON "public"."oasis_node" FROM "anon";

REVOKE DELETE ON "public"."oasis_node" FROM "authenticated";

REVOKE TRUNCATE ON "public"."oasis_node" FROM "authenticated";

REVOKE TRIGGER ON "public"."oasis_node" FROM "authenticated";

REVOKE DELETE ON "public"."oasis_node" FROM "service_role";

REVOKE TRUNCATE ON "public"."oasis_node" FROM "service_role";

REVOKE TRIGGER ON "public"."oasis_node" FROM "service_role";

REVOKE DELETE ON "public"."oasis_node_nodetype" FROM "postgres";

REVOKE TRUNCATE ON "public"."oasis_node_nodetype" FROM "postgres";

REVOKE TRIGGER ON "public"."oasis_node_nodetype" FROM "postgres";

REVOKE DELETE ON "public"."oasis_node_nodetype" FROM "anon";

REVOKE TRUNCATE ON "public"."oasis_node_nodetype" FROM "anon";

REVOKE TRIGGER ON "public"."oasis_node_nodetype" FROM "anon";

REVOKE DELETE ON "public"."oasis_node_nodetype" FROM "authenticated";

REVOKE TRUNCATE ON "public"."oasis_node_nodetype" FROM "authenticated";

REVOKE TRIGGER ON "public"."oasis_node_nodetype" FROM "authenticated";

REVOKE DELETE ON "public"."oasis_node_nodetype" FROM "service_role";

REVOKE TRUNCATE ON "public"."oasis_node_nodetype" FROM "service_role";

REVOKE TRIGGER ON "public"."oasis_node_nodetype" FROM "service_role";

UPDATE alembic_version SET version_num='20260121_02_rls' WHERE alembic_version.version_num = '20260121_01_rls';

COMMIT;

