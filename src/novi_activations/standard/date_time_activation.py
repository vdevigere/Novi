import json
from datetime import datetime

from novi.core import BaseActivation


class DateTimeActivation(BaseActivation):
    def __init__(self, cfg: str = None):
        configuration = json.loads(cfg)
        if {'startDateTime', 'endDateTime', 'format'} <= configuration.keys():
            datetimeformat = configuration.get('format')
            configuration['startDateTime'] = datetime.strptime(configuration['startDateTime'], datetimeformat)
            configuration['endDateTime'] = datetime.strptime(configuration['endDateTime'], datetimeformat)
            super().__init__(configuration)

    def evaluate(self, context: dict = None) -> bool:
        if {'currentDateTime'} <= context.keys():
            context['currentDateTime'] = datetime.strptime(context['currentDateTime'], self.config['format'])
            if self.config['startDateTime'] <= context['currentDateTime'] < self.config['endDateTime']:
                return True
            else:
                return False
