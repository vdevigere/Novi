from typing import List

from sqlalchemy import String, Boolean, ForeignKey, Column, Table
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, MappedAsDataclass, relationship


class Base(MappedAsDataclass, DeclarativeBase):
    pass


flags_activations = Table(
    "flags_activations",
    Base.metadata,
    Column("flag_id", ForeignKey("flags.id")),
    Column("activation_id", ForeignKey("activations.id")),
)


class Activation(Base):
    __tablename__ = "activations"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    class_name: Mapped[str] = mapped_column(String, nullable=False)
    config: Mapped[str] = mapped_column(String)


class Flag(Base):
    __tablename__ = "flags"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    activations: Mapped[List[Activation]] = relationship(secondary=flags_activations, lazy="joined")
    status: Mapped[bool] = mapped_column(Boolean, default=True)
