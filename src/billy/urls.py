from django.urls import path
from . import views
from .views import MyTokenObtainPairView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('register', views.RegisterView.as_view()),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('accounts', views.AccountsMethods.as_view()),
    path('accounts/<int:pk>', views.AccountMethods.as_view()),

    path('movements', views.MovementsMethods.as_view()),
    path('movements/<int:pk>', views.MovementMethods.as_view()),

    path('summary', views.SummariesMethods.as_view()),
    path('summary/<int:pk>', views.SummaryMethods.as_view()),
]
