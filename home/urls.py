from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name ="home"
urlpatterns = [
    path('',views.home,name='home'),
    path('login/',views.login_user,name='login'),
    path('logout/',views.logout_user,name='logout'),
    path('register/',views.register_user,name='register'),
    path('profile/',views.user_profile, name = 'profile'),
    path('detail/<int:id>', views.book_detail, name='book-detail'),
    path('edit-profile', views.edit_profile, name = 'edit-profile'),
    path('afterRegister/',views.afterRegister,name='afterRegister'),

]

 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)