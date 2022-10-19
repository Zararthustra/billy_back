from django.urls import path
from . import views

urlpatterns = [
    path('register', views.RegisterView.as_view()),
    
    path('accounts', views.AccountsMethods.as_view()),
    path('accounts/<int:pk>', views.AccountMethods.as_view()),

    path('movements', views.MovementsMethods.as_view()),
    path('movements/<int:pk>', views.MovementMethods.as_view()),

    path('summary', views.SummariesMethods.as_view()),
    path('summary/<int:pk>', views.SummaryMethods.as_view()),
]
