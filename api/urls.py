from django.urls import path
from api import views as api_views

app_name = 'api'

urlpatterns = [
    # /api/v1/five-start-stats
    path('five-star-stats', api_views.FiveStarStats.as_view(), name='stats'),
    # /api/v1/metrics
    path('metrics', api_views.Metrics.as_view(), name='metrics'),
]
