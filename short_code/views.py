from django.http import HttpResponseRedirect
from django.utils import timezone
from django.db import transaction
from django.db.models import F
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status

from .helpers import generate_and_save_next_short_code
from .models import ShortCode
from .serializers import ShortCodeSerializer, CustomAPIException


class ShortCodeEndpoint(APIView):
    def post(self, request):
        serializer = ShortCodeSerializer(data=request.data)
        serializer.is_valid()

        if not serializer.is_valid(raise_exception=False):
            raise ValidationError(detail=serializer.errors)

        full_url = serializer.validated_data.get('full_url', None)
        short_code_provided_by_user = serializer.validated_data.get('short_code', None)

        if short_code_provided_by_user:
            short_code, created = ShortCode.objects.get_or_create(
                short_code=short_code_provided_by_user,
                defaults={
                    "full_url": full_url,
                    "redirect_count": 0,
                }
            )
            if not created:
                raise CustomAPIException(f"Short code already in use", 409)
        else:
            short_code = generate_and_save_next_short_code(full_url)
        return Response({"shortcode": short_code.short_code}, status=status.HTTP_201_CREATED)

    def get(self, request, short_code=None):
        try:
            short_code = ShortCode.objects.get(
                short_code=short_code
            )
            serializer = ShortCodeSerializer(short_code)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ShortCode.DoesNotExist:
            raise CustomAPIException(f"Short code not found", 404)


@api_view(["GET"])
def redirect_by_short_code(request, short_code):
    try:
        short_code = ShortCode.objects.get(
            short_code=short_code
        )
        with transaction.atomic():
            short_code.redirect_count = F("redirect_count") + 1
            short_code.last_redirect_at = timezone.now()
            short_code.save(update_fields=["redirect_count", "last_redirect_at"])
        return HttpResponseRedirect(short_code.full_url)
    except ShortCode.DoesNotExist:
        raise CustomAPIException(f"Short code not found", 404)
