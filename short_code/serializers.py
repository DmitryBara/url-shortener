from django.conf import settings
from rest_framework import serializers
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from .utils import CustomAPIException, DefaultSerializerField
from .models import ShortCode


class ShortCodeSerializer(serializers.ModelSerializer):
    url = DefaultSerializerField(required=False, source='full_url', write_only=True)
    shortcode = DefaultSerializerField(required=False, source='short_code', write_only=True)
    created = serializers.SerializerMethodField(read_only=True)
    lastRedirect = serializers.SerializerMethodField(read_only=True)
    redirectCount = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ShortCode
        fields = ['url', 'shortcode', 'created', 'lastRedirect', 'redirectCount']

    def get_created(self, obj):
        return obj.created_at

    def get_lastRedirect(self, obj):
        return obj.last_redirect_at

    def get_redirectCount(self, obj):
        return obj.redirect_count

    def validate(self, attrs):

        full_url = attrs.get('full_url', None)
        if not full_url:
            raise CustomAPIException("Url not present", 400)
        if type(full_url) is not str:
            raise CustomAPIException("The provided url is invalid",  412)
        try:
            URLValidator()(full_url)
        except ValidationError:
            raise CustomAPIException("The provided url is invalid", 412)

        short_code = attrs.get('short_code', None)
        if short_code:
            if type(short_code) is not str:
                raise CustomAPIException("The provided short code is invalid", 412)
            for symbol in short_code:
                if settings.SORTED_ALPHABET.find(symbol) == -1:
                    raise CustomAPIException(f"The provided short code is invalid. Unexpected symbol '{symbol}'", 412)

        if short_code and settings.CHECK_SHORT_CODE_LENGTH_PROVIDED_BY_USER:
            if len(short_code) != settings.REQUESTED_SHORT_CODE_LENGTH:
                raise CustomAPIException(f"The provided short code is invalid. Unexpected length {len(short_code)}", 412)

        return attrs
