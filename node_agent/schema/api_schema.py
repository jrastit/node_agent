from pydantic import BaseModel, ConfigDict


class ServerUpsertSchema(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: int | None = None
    name: str
    cloud: str | None = None
    cloud_name: str | None = None
    ip: str | None = None
    organisation_id: int | None = None


class EntrypointUpsertSchema(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: int | None = None
    name: str
    user: str | None = None
    path: str | None = None
    ssh_id: str | None = None
    server_id: int | None = None


class OasisNodeUpsertSchema(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: int | None = None
    name: str
    entity_id: int | None = None
    nodetype_id: list[int] | None = None


class OasisNodetypeUpsertSchema(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: int | None = None
    name: str
    network_id: int | None = None


class OasisNetworkUpsertSchema(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: int | None = None
    name: str


class OasisEntityUpsertSchema(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: int | None = None
    name: str


api_schemas = {
    "server_put": ServerUpsertSchema,
    "entrypoint_put": EntrypointUpsertSchema,
    "oasis_node_put": OasisNodeUpsertSchema,
    "oasis_nodetype_put": OasisNodetypeUpsertSchema,
    "oasis_network_put": OasisNetworkUpsertSchema,
    "oasis_entity_put": OasisEntityUpsertSchema,
}
