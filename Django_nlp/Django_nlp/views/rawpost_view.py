from rest_framework.generics import ListAPIView, RetrieveAPIView
from ..serializers import RawSerializer
from ..models import Raw


class RawPostList(ListAPIView):
    queryset = Raw.objects.all().order_by('post_time').reverse()
    serializer_class = RawSerializer


class RawPostRet(RetrieveAPIView):
    queryset = Raw.objects.all()
    serializer_class = RawSerializer
