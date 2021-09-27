import sys
from django.apps import AppConfig


class ShortCodeConfig(AppConfig):
    name = 'short_code'

    def ready(self):
        if not ('runserver' in sys.argv):
            return

        from short_code.models import DynamicConfig
        try:
            dynamic_config_initial_parameters_record = DynamicConfig.objects.get(
                name=DynamicConfig.CURRENT_INITIAL_PARAMETERS_ID
            )
            dynamic_config_initial_parameters_record.delete()
        except DynamicConfig.DoesNotExist:
            pass
