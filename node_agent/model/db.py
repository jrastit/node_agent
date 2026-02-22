import typing
from typing import Annotated

from sqlalchemy import UUID
from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    create_engine,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, MappedAsDataclass, relationship
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import scoped_session, sessionmaker


class Database:
    Integer = Integer
    DateTime = DateTime
    String = String
    Boolean = Boolean
    ForeignKey = ForeignKey
    func = func

    def __init__(self):
        self.engine = None
        self.session = scoped_session(
            sessionmaker(
                autocommit=False, autoflush=False, expire_on_commit=False
            )
        )

    def init(self, database_uri: str, engine_options: dict | None = None):
        if self.engine is not None:
            return
        options = engine_options or {}
        self.engine = create_engine(database_uri, **options)
        self.session.configure(bind=self.engine)

    def remove_session(self):
        self.session.remove()


db = Database()

intpk = Annotated[int, mapped_column(primary_key=True)]


def column_id():
    return mapped_column(
        db.Integer,
        primary_key=True,
        server_default=None,
        nullable=False,
        init=None,
        insert_sentinel=False,
    )


def column_uuid():
    return mapped_column(
        UUID(as_uuid=True),
        unique=True,
        nullable=True,
    )


def column_time_created():
    return mapped_column(
        db.DateTime,
        server_default=db.func.now(),
        default=None,
    )


def column_time_updated():
    return mapped_column(
        db.DateTime,
        server_default=db.func.now(),
        onupdate=db.func.current_timestamp(),
        default=None,
    )


def column_name():
    return mapped_column(
        db.String,
        unique=False,
        nullable=False,
        default=None,
    )


def column_string_null() -> Mapped[typing.Optional[str]]:
    return mapped_column(
        db.String,
        nullable=True,
        default=None,
    )


def column_bool_null() -> Mapped[typing.Optional[str]]:
    return mapped_column(
        db.Boolean,
        nullable=True,
        default=None,
    )


def column_foreign_key(key, primary_key=False, ondelete=None):
    if primary_key:
        nullable = False
    else:
        nullable = True
    fk = (
        db.ForeignKey(key, ondelete=ondelete)
        if ondelete
        else db.ForeignKey(key)
    )
    return mapped_column(
        db.Integer,
        fk,
        primary_key=primary_key,
        nullable=nullable,
        default=None,
    )


def column_relationship_many_to_many(
    mapped, secondary, back_populates=None, lazy="select"
):
    return relationship(
        mapped,
        back_populates=back_populates,
        secondary=secondary,
        default_factory=list,
        lazy=lazy,
    )


def column_relationship_list(mapped, back_populates=None, foreign_keys=None):
    return relationship(
        mapped,
        back_populates=back_populates,
        foreign_keys=foreign_keys,
        default_factory=list,
        repr=False,  # évite repr récursif
        compare=False,  # évite eq récursif (dataclass)
    )


def column_relationship_list_req(
    mapped, back_populates=None, foreign_keys=None
):
    return relationship(
        mapped,
        back_populates=back_populates,
        foreign_keys=foreign_keys,
        default_factory=list,
    )


def column_relationship(foreign_keys=None):
    return relationship(default=None, foreign_keys=foreign_keys)


class Base(MappedAsDataclass, DeclarativeBase):
    pass
