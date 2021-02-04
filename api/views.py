# Create your views here.
import os

from rest_framework import generics

from api.models import Files
from api.serializers import FileSerializer
from djangoHealthAnalytics.settings import BASE_DIR


class FileList(generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Files.objects.all()
    serializer_class = FileSerializer
# http http://127.0.0.1:8000/api/v1/files/ 'Authorization: Token 6c7494f9eb960d9027c12b282e57f06e7b974cc7'
