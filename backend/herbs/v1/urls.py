from django.urls import path

from .views import (
    HerbsListView,
    HerbDetailView,
    HerbOfferView,
    CategoryListView,
    TagListView,
    SymptomListView,
)

app_name = 'herbs-v1'

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='herbs_categories'),
    path('tags/', TagListView.as_view(), name='herbs_tags'),
    path('symptoms/', SymptomListView.as_view(), name='herbs_symptoms'),
    path('', HerbsListView.as_view(), name='herbs_list'),
    path('<slug:slug>/', HerbDetailView.as_view(), name='herbs_detail'),
    path('<slug:slug>/offers/', HerbOfferView.as_view(), name='herbs_offers'),
]
