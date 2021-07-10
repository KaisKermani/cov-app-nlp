from rest_framework.generics import ListAPIView
from ..serializers import TestSerializer
from ..models import Test


class TestList(ListAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
