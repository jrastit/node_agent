from node_agent.service.supabase.supabase_client import (
    supabase_client,
    supabase_public_client,
)


def test_psql_discover_list_public_tables():
    admin_client = supabase_client()
    response = admin_client.rpc("list_public_tables").execute()
    assert response is not None, "No response from psql_discover"
    assert response.data is not None, "No data in response from psql_discover"
    assert isinstance(response.data, list), "Response data is not a list"
    assert len(response.data) > 0, "No tables discovered by psql_discover"
    for table in response.data:
        assert (
            "table_name" in table
        ), "Table name not found in psql_discover response"
    public_client = supabase_public_client()
    response_public = public_client.rpc("list_public_tables").execute()
    assert (
        response_public is not None
    ), "No response from psql_discover with public client - this should still work"
    assert (
        response_public.data is not None
    ), "No data in response from psql_discover with public client - this should still work"
    assert isinstance(
        response_public.data, list
    ), "Response data is not a list from psql_discover with public client - this should still work"
    assert (
        len(response_public.data) > 0
    ), "No tables discovered by psql_discover with public client - this should still work"
    for table in response_public.data:
        assert (
            "table_name" in table
        ), "Table name not found in psql_discover response with public client - this should still work"
