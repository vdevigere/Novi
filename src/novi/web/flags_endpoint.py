import dataclasses

from flask import Blueprint

from novi.client import flag
from novi.core.models import FlagModel

blueprint = Blueprint("flags", __name__)


@blueprint.route("/flags", methods=['GET'])
def all_flags() -> list[FlagModel]:
    return flag.get_flags()


@blueprint.route("/flags/<flag_name>", methods=['GET'])
def flags_by_name(flag_name: str) -> dict:
    return dataclasses.asdict(flag.get_flag_by_name(flag_name))
