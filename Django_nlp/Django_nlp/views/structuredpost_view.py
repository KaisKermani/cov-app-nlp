from rest_framework.generics import ListAPIView, RetrieveAPIView
from ..serializers import StructuredSerializer
from ..models import Structured


class StructuredPostList(ListAPIView):
    queryset = Structured.objects.all().select_related('id').order_by('id__post_time').reverse()
    serializer_class = StructuredSerializer


class StructuredPostRet(RetrieveAPIView):
    queryset = Structured.objects.all()
    serializer_class = StructuredSerializer
