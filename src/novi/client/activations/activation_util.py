import logging

from novi.core import discovered_activations, BaseActivation
from novi.core.models import ActivationModel


def apply_operation_on_all_activations(operation: str, activations: list[ActivationModel],
                                       context: dict = None) -> bool:
    status = None
    for activation in activations:
        logging.getLogger(__name__).debug(f"Discovered Activations: {discovered_activations}")
        if activation.class_name in discovered_activations:
            # instantiate class
            obj: BaseActivation = discovered_activations[activation.class_name](activation.config)
            # evaluate with provided context
            logging.getLogger(__name__).debug(f"Applying Activation: {activation.name}")
            evaluated_status = obj.evaluate(context)
            # and with previously evaluated status
            logging.getLogger(__name__).debug(f"Status Before Eval {status}")
            match operation:
                case 'and':
                    status = evaluated_status if status is None else (status and evaluated_status)
                case 'or':
                    status = evaluated_status if status is None else (status or evaluated_status)
                case default:
                    status = status
            logging.getLogger(__name__).debug(f"Status After applying {evaluated_status} = {status}")
        else:
            logging.getLogger(__name__).debug(f"{activation.class_name} not found")
    return status


def and_all_activations(activations: list[ActivationModel], context: dict = None) -> bool:
    return apply_operation_on_all_activations('and', activations, context)


def or_all_activations(activations: list[ActivationModel], context: dict = None) -> bool:
    return apply_operation_on_all_activations('or', activations, context)
