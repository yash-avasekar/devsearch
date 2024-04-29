from . import views

from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    # token will generator token
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # refresh token generates new token
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


    path('' ,views.getProjects),
    path('project/<str:pk>' ,views.getProject), # single project
    path('project/<str:pk>/vote/' ,views.projectVote), # 
]