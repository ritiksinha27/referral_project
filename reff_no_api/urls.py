from django.urls import path
from .views import *
urlpatterns = [
   path('', home, name='home'),
#    path('<str:cust_str>', home_str, name='home_str'),
   path('login/', user_login, name='user_login'),
   path('logout/', user_logout, name='user_logout'),
   path('sign_up/', user_register.as_view(), name='user_register'),
   path('sign_up/<str:ref_id>/', user_register.as_view(), name='ref_register'),
   path('profile/', user_dashboard, name='user_dash'),
   path('admin_login/',admin_login, name='admin_login'),
   path('admin_dash/',admin_dash, name='admin_dash'),
   path('add_points/<int:usr_str_id>/',add_points, name='add_points'),
   path('valid_user/<str:usr_name>/',username_validate, name='valid_user'),
   path('valid_mob/<str:mob_no>/',mobile_validate, name='valid_mob'),
]
