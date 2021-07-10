"""Django_test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .views.test_view import TestList
from .views.rawpost_view import RawPostList, RawPostRet
from .views.structuredpost_view import StructuredPostList, StructuredPostRet
from .views.fullpost_view import FullPostInfo
from django.views.generic.base import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/api/meta/')),
    path('api/test/', TestList.as_view(), name='test'),
    path('api/meta/', RawPostList.as_view(), name='meta'),
    path('api/meta/<str:pk>/', RawPostRet.as_view(), name='meta'),
    path('api/structured/', StructuredPostList.as_view(), name='structured'),
    path('api/structured/<str:pk>/', StructuredPostRet.as_view(), name='single_structured'),
    path('api/post/<str:pk>/', FullPostInfo.as_view(), name='full'),
]
