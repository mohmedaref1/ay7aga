from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('blog/getResponse',views.getResponse,name='getResponse'),
    path('accounts/login/', views.loginn, name='loginn'),
    path('logout', views.logoutt, name='logout'),
    path('reg', views.reg, name='reg'),
    path('status', views.status, name='status'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
]