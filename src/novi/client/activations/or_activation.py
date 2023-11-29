import logging

from novi.client.activations.base_combination_activation import BaseCombinationActivation
from novi.core import discovered_activations, BaseActivation, register


@register
class OrActivation(BaseCombinationActivation):
    def evaluate(self, context: dict = None) -> bool:
        status = None
        for activation in self.config:
            if activation.class_name in discovered_activations:
                logging.getLogger(__name__).debug(f"Applying Activation: {activation.name}")
                obj: BaseActivation = discovered_activations[activation.class_name](activation.config)
                evaluated_status = obj.evaluate(context)
                logging.getLogger(__name__).debug(f"Status Before Eval {status}")
                if status is None:
                    status = evaluated_status
                else:
                    status = status or evaluated_status
                logging.getLogger(__name__).debug(f"Status After AND with {evaluated_status} = {status}")
        return status
