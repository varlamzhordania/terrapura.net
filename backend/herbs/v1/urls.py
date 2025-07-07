from django.urls import path

from .views import (
    HerbsList,
    HerbDetail,
    CategoryList,
    TagList,
    SymptomList,
)

app_name = 'herbs-v1'

urlpatterns = [
    path('categories/', CategoryList.as_view(), name='herbs_categories'),
    path('tags/', TagList.as_view(), name='herbs_tags'),
    path('symptoms/', SymptomList.as_view(), name='herbs_symptoms'),
    path('', HerbsList.as_view(), name='herbs_list'),
    path('<slug:slug>/', HerbDetail.as_view(), name='herbs_detail'),
]
