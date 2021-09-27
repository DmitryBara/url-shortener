from rest_framework import serializers
from rest_framework.exceptions import APIException


# Use this for custom exceptions 'status_code' and 'detail' (technical requirements)
class CustomAPIException(APIException):
    def __init__(self, detail, status_code):
        self.status_code = status_code
        self.detail = detail


# Use this for custom field validation (technical requirements)
class DefaultSerializerField(serializers.Field):
    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        return data
