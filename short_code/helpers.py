from rest_framework.exceptions import APIException
from django.db import IntegrityError, transaction
from short_code.models import InitialParametersState, ShortCode, DynamicConfig
from short_code.converter import Converter
from django.conf import settings


def save_initial_parameters_id_to_dynamic_config():

    alphabet = settings.SORTED_ALPHABET
    requested_short_code_length = settings.REQUESTED_SHORT_CODE_LENGTH

    lowest_number_converted_to_short_code = ''.join(
        [alphabet[0] for _ in range(requested_short_code_length)])
    highest_number_converted_to_short_code = ''.join(
        [alphabet[-1] for _ in range(requested_short_code_length)])

    min_number_from_range = Converter.other_base_to_decimal(lowest_number_converted_to_short_code)
    max_number_from_range = Converter.other_base_to_decimal(highest_number_converted_to_short_code)

    initial_parameters, created = InitialParametersState.objects.get_or_create(
        alphabet_sorted=alphabet,
        requested_short_code_length=requested_short_code_length,
        defaults={
            'min_number_from_range': min_number_from_range,
            'max_number_from_range': max_number_from_range,
            'last_number_converted_to_short_code': min_number_from_range - 1,
        },
    )

    DynamicConfig.objects.update_or_create(
        name=DynamicConfig.CURRENT_INITIAL_PARAMETERS_ID,
        defaults={
            'value': initial_parameters.id
        },
    )

    return initial_parameters.id


def generate_and_save_next_short_code(full_url: str):

    try:
        initial_parameters_id = DynamicConfig.objects.get(name=DynamicConfig.CURRENT_INITIAL_PARAMETERS_ID).value
    except DynamicConfig.DoesNotExist:
        initial_parameters_id = save_initial_parameters_id_to_dynamic_config()

    initial_parameters_state = InitialParametersState.objects.get(id=initial_parameters_id)
    number_candidate = initial_parameters_state.last_number_converted_to_short_code + 1
    created = False

    while not created:
        if number_candidate >= initial_parameters_state.max_number_from_range:
            raise APIException('New unique string could not be generated. Change initial parameters and reload app.')

        new_generated_string = Converter.decimal_to_other_base(number_candidate)

        try:
            ShortCode.objects.get(
                short_code=new_generated_string,
            )
            number_candidate += 1
            continue
        except ShortCode.DoesNotExist:
            try:
                with transaction.atomic():
                    short_code = ShortCode.objects.create(
                        short_code=new_generated_string,
                        full_url=full_url,
                        redirect_count=0,
                    )

                    initial_parameters_state.last_number_converted_to_short_code = number_candidate
                    initial_parameters_state.save(update_fields=["last_number_converted_to_short_code"])

                    return short_code
            except IntegrityError:
                """
                If current ShortCode instance not created (from number_candidate)
                and field 'InitialParameters.last_number_converted_to_short_code' not increased (to number_candidate)
                in one atomic transaction (finished with IntegrityError).
                In this case we should recall 'generate_and_save_next_short_code' function.

                TODO: change mechanism to queue (RabbitMQ) to prevent IntegrityError and make more clean realization 
                """
                generate_and_save_next_short_code(full_url)


