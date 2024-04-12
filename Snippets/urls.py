from django.urls import path
from .views import UserDetails ,CustomAuthToken,snippets
# from rest_framework.authtoken import views
    
urlpatterns = [
    path('user', UserDetails.as_view(),name='user_login'),
    path('api/token/auth', CustomAuthToken.as_view(),name='token')
    path('api', snippets.as_view(),name='get_or_create'),
    path('api/<int:id>', snippets.as_view(),name='update_or_delete' ),
]