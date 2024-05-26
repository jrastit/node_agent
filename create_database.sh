#!/bin/bash
if [ "$(whoami)" != "postgres" ]; then
        echo "Script must be run as user: postgres"
        exit 255
fi


psql -c "create user node_agent with encrypted password '$DB_PASSWORD'"

psql -c "create database node_agent"
psql -c "grant all privileges on database node_agent to node_agent"

psql -c "ALTER DATABASE node_agent OWNER TO node_agent;"

psql -c "create database node_agent_test"
psql -c "grant all privileges on database node_agent_test to node_agent"


psql -c "ALTER DATABASE node_agent_test OWNER TO node_agent;"