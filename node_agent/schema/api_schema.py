from pydantic import BaseModel, ConfigDict, model_validator


class ServerUpsertSchema(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: int | None = None
    name: str
    cloud: str | None = None
    cloud_name: str | None = None
    ip: str | None = None
    hostname: str | None = None
    fqdn: str | None = None
    os: str | None = None
    kernel: str | None = None
    cpu_cores: int | None = None
    ram_total_mb: int | None = None
    organization_id: int | None = None

    @model_validator(mode="after")
    def validate_create_requires_organization(self):
        if self.id is None and self.organization_id is None:
            raise ValueError(
                "organization_id is required when creating a server"
            )
        return self


class EntrypointUpsertSchema(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: int | None = None
    name: str
    user: str | None = None
    path: str | None = None
    ssh_id: str | None = None
    server_id: int | None = None


class ServerHostUpsertSchema(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: int | None = None
    ip: str | None = None
    description: str | None = None
    server_id: int | None = None


class ServerIpUpsertSchema(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: int | None = None
    port: str | None = None
    description: str | None = None
    server_host_id: int | None = None


class ServerSSHUpsertSchema(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: int | None = None
    user_name: str | None = None
    description: str | None = None
    server_port_id: int | None = None


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


class OrganizationUpsertSchema(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: int | None = None
    name: str
    parent_id: int | None = None


api_schemas = {
    "server_put": ServerUpsertSchema,
    "entrypoint_put": EntrypointUpsertSchema,
    "server_host_put": ServerHostUpsertSchema,
    "server_ip_put": ServerIpUpsertSchema,
    "server_ssh_put": ServerSSHUpsertSchema,
    "oasis_node_put": OasisNodeUpsertSchema,
    "oasis_nodetype_put": OasisNodetypeUpsertSchema,
    "oasis_network_put": OasisNetworkUpsertSchema,
    "oasis_entity_put": OasisEntityUpsertSchema,
    "organization_put": OrganizationUpsertSchema,
}
