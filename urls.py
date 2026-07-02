from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .import views

urlpatterns = [
 	path('', views.home, name='home'),
    path('base/', views.base, name='base'),
    path('UserLogin/', views.UserLogin, name='UserLogin'),
    path('UserRegisteration/', views.UserRegisteration, name='UserRegisteration'),
    path('Prediction/', views.Prediction, name='Prediction'),
    path('View_Persona/', views.View_Persona, name='View_Persona'),
    path('Give_Recommendations/', views.Give_Recommendations, name='Give_Recommendations'),
    path('View_Data/', views.View_Data, name='View_Data'),
    path('Share/<int:id>', views.Share, name='Share'),
    path('Logout/', views.Logout, name='Logout'),
    path('detect/', views.detect, name='detect'),
    path('cluster0/', views.cluster0, name='cluster0'),
    path('cluster1/', views.cluster1, name='cluster1'),
    path('cluster2/', views.cluster2, name='cluster2'),
    path('cluster3/', views.cluster3, name='cluster3'),
]
urlpatterns = urlpatterns + static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)