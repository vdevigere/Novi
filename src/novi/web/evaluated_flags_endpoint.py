import dataclasses

from flask import Blueprint, request

from novi.client import flag
from novi.core.models import FlagModel

blueprint = Blueprint("evaluatedFlags", __name__)


@blueprint.route("/evaluatedFlags", methods=['POST'])
def all_flags() -> list[FlagModel]:
    context = request.get_json(silent=True)
    return flag.get_flags(context, evaluate=True)


@blueprint.route("/evaluatedFlags/<flag_name>", methods=['POST'])
def flags_by_name(flag_name: str) -> dict:
    context = request.get_json(silent=True)
    return dataclasses.asdict(flag.get_flag_by_name(flag_name, context=context, evaluate=True))
