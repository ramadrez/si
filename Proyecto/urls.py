"""
URL configuration for Proyecto project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path,include
from django.conf import settings
from django.views.static import serve
from APP.views import IndexView
from APP.views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls ),
    path('', include('APP.urls')),
    
    #Rutas para PDF
    path('',IndexView),
    path('generar-pdf_resguardo/', generar_pdf_resguardo, name='generar_pdf_resguardo'),
    path('generar-pdf_voluntarios/', generar_pdf_voluntarios, name='generar_pdf_voluntarios'),
    path('generar-pdf_propio/<int:user_id>', generar_pdf_propio, name='generar_pdf_propio'),
    path('generar-pdf_adopciones/', generar_pdf_adopciones, name='generar_pdf_adopciones'),
    path('generar-pdf_adoptantes/', generar_pdf_adoptantes, name='generar_pdf_adoptantes'),
    path('generar-pdf_ficha/<str:adopcion_id>/', generar_pdf_ficha, name='generar_pdf_ficha'),
    path('generar-pdf_sin_esterilizar/', generar_pdf_sin_esterilizar, name='generar_pdf_sin_esterilizar'),
    

    path('password_reset/', 
         auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'), 
         name='password_reset'),
    
    path('password_reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='registration/password_done.html'), 
         name='password_reset_done'),
    
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_confirm.html'), 
         name='password_reset_confirm'),
    
    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_complete.html'), 
         name='password_reset_complete'),
      
]

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve,{
        'document_root': settings.MEDIA_ROOT,
    })
]