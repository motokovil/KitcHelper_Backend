from django.urls import path
from ..viewsData.viewMeasure import ViewMeasureGet

urlpatterns = [
    path('', ViewMeasureGet.as_view())
]
