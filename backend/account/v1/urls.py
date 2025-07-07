from django.urls import path

from .views import (
    RetrieveSelfApiView
)

app_name = 'account-v1'

urlpatterns = [
    path('me/', RetrieveSelfApiView.as_view(), name='retrieve_self'),
]
