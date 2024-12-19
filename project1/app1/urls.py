from django.urls import path
from . import views

urlpatterns = [
    path('login',views.login,name='login'),
    path('sigin/',views.sig,name='signin'),
    path('home/',views.home,name='home'),
    path('myadmin/',views.myadmin,name='admin1'),
    path('logout/',views.logout,name='logout'),
    path('edituser/<int:id>',views.edituser,name='edituser'), 
    path('delete/<int:id>',views.delete,name='delete'),
    path('search/',views.searchuser,name='searchuser'),
    path('adduser/',views.aadduser,name='adduser'),
    
]
