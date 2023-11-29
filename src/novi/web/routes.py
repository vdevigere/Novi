import dataclasses
import json

from flask import Blueprint, request

from novi.client import flag
from novi.core.models import Flag

blueprint = Blueprint("flags", __name__)


@blueprint.route("/flags", methods=['POST'])
def all_flags() -> list[Flag]:
    evaluate = request.args.get('evaluate', default=True, type=json.loads)
    context = request.get_json(silent=True)
    return flag.get_flags(context, evaluate=evaluate)


@blueprint.route("/flags/<flag_name>", methods=['POST'])
def flags_by_name(flag_name: str) -> dict:
    evaluate = request.args.get('evaluate', default=True, type=json.loads)
    context = request.get_json(silent=True)
    return dataclasses.asdict(flag.get_flag_by_name(flag_name, context=context, evaluate=evaluate))
