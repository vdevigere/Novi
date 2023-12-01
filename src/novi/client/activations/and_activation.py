from novi.client.activations import activation_util
from novi.client.activations.base_combination_activation import BaseCombinationActivation
from novi.core import register


@register
class AndActivation(BaseCombinationActivation):
    def evaluate(self, context: dict = None) -> bool:
        return activation_util.and_all_activations(self.config, context)
