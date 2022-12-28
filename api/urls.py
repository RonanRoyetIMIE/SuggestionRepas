# from django.urls import include, path, re_path
# from api import views 
 
# urlpatterns = [ 
#     path('users', views.users_list),
#     re_path(r'^user/(?P<pk>[0-9]+)$', views.user_detail),
# ]

from django.urls import include, path
from rest_framework import routers
from api import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet, 'users')
router.register(r'register', views.RegisterViewSet, 'register')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', views.LoginView.as_view()),
    path('logout/', views.LogoutView.as_view()),
]