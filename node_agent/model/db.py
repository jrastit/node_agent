import typing
from typing import Annotated

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, MappedAsDataclass, relationship
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase


db = SQLAlchemy()

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


def column_foreign_key(key, primary_key=False):
    if primary_key:
        nullable = False
    else:
        nullable = True
    return mapped_column(
        db.Integer,
        db.ForeignKey(key),
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
    )


def column_relationship(foreign_keys=None):
    return relationship(default=None, foreign_keys=foreign_keys)


class Base(MappedAsDataclass, DeclarativeBase):
    pass
