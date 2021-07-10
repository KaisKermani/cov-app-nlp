from rest_framework.generics import RetrieveAPIView
from django.http import HttpResponse
from django.core.serializers import serialize
from ..serializers import StructuredSerializer, RawSerializer, PostSerializer
from ..models import Structured, Raw


class FullPostInfo(RetrieveAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        res = Structured.objects.select_related('id')
        return res


