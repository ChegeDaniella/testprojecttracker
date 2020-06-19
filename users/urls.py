from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views
from .views import UserLoginView

urlpatterns = [
  path('login',UserLoginView.as_view(), name='login'),
  path('users', views.UsersList.as_view(),name='users-api'),
  path('logout',views.LogoutView, name='logout'),
  path('rest-auth/', include('rest_auth.urls')),


]
