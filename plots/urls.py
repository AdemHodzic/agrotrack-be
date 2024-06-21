from django.urls import path
from .views import PlotListView, PlotDetailView, LoginView

urlpatterns = [
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/plots/<int:user_id>/', PlotDetailView.as_view(), name='plot-detail'),
]