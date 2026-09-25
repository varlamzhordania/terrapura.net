from django.urls import path, include
from .views import PartnerDetailAPIView

app_name = 'partners-v1'

urlpatterns = [
    path(
        "<int:pk>/",
        PartnerDetailAPIView.as_view(),
        name="partner_detail"
    ),

    path('', include('partners.v1.seller.urls')),

]
