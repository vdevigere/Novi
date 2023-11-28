import dataclasses

from flask import Blueprint

from novi.client.dbclient import DbClient
from novi.core.models import Flag

blueprint = Blueprint("flags", __name__)


@blueprint.route("/flags")
def all_flags() -> list[Flag]:
    flags = DbClient().get_flags()
    return flags


@blueprint.route("/flags/<flag_name>")
def flags_by_name(flag_name: str) -> dict:
    flag: Flag = DbClient().get_flag_by_name(flag_name)
    return dataclasses.asdict(flag)
