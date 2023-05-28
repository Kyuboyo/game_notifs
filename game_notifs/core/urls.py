from django.urls import path
from .views import *

urlpatterns = [
    path('offers/', OffersView.as_view(), name="offers"),
    path('pull_data/', PullData.as_view(), name="pull_data"),
    path('store_to_empty_db/', StoreToEmptyDB.as_view(), name="store_to_empty_db"),
]