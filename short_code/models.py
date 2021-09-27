from django.db import models


class ShortCode(models.Model):
    short_code = models.CharField(max_length=30, unique=True)
    full_url = models.URLField(max_length=300)
    redirect_count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_redirect_at = models.DateTimeField(blank=True, null=True)

    class Meta(object):
        ordering = ('-created_at', )

    def __str__(self):
        return self.short_code


""" 
Next two tables keep already calculated state (depends on previous generated strings and initial parameters).
This parameters could be managed in '.env' file.
Generating of next string 'short_code' continue from 'last_number_converted_to_short_code' for current parameters.
See details in 'converter.py'
"""


class InitialParametersState(models.Model):
    alphabet_sorted = models.CharField(max_length=300)
    requested_short_code_length = models.IntegerField()
    min_number_from_range = models.BigIntegerField()
    max_number_from_range = models.BigIntegerField()
    last_number_converted_to_short_code = models.BigIntegerField()

    class Meta:
        unique_together = ('alphabet_sorted', 'requested_short_code_length')

    def __str__(self):
        return f'{self.alphabet_sorted} : {self.requested_short_code_length}'


class DynamicConfig(models.Model):
    CURRENT_INITIAL_PARAMETERS_ID = 'current_initial_parameters_id'
    CONFIG_VARIABLES_CHOICES = (
        (CURRENT_INITIAL_PARAMETERS_ID, u'Current Initial Parameters Id'),
    )

    name = models.CharField(max_length=30, unique=True, choices=CONFIG_VARIABLES_CHOICES)
    value = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.name} : {self.value}'







