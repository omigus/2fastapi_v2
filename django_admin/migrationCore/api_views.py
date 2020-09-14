from rest_framework import viewsets
from . import models
from . import serializers

class CompanyViewset(viewsets.ModelViewSet):
    queryset = models.Company.objects.all()
    serializer_class = serializers.CompanySerializer
