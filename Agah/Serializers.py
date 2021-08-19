from rest_framework import serializers

from Agah.models import Responder


class Responder_Firstname_Serialier(serializers.ModelSerializer):
    class Meta:
        model = Responder
        fields = ('firstname','lastname',)
