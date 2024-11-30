# bakery_app/utils.py

import decimal
import json
from django.core.serializers.json import DjangoJSONEncoder

class CustomDecimalEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)  # Преобразуем Decimal в строку
        return super().default(obj)
