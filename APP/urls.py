from django.urls import path
from .views import (
    AnimalListView, AnimalCreateView, AnimalUpdateView, AnimalDeleteAjaxView,
    AdoptanteListView, AdoptanteCreateView, AdoptanteUpdateView, AdoptanteDeleteAjaxView,
    AdopcionesListView, AdopcionesCreateView, AdopcionesDeleteView,
    VoluntariosListView, VoluntarioEditView, VoluntarioDeleteView,
    UserAnimalesListView, UserAnimalCreateView, UserAnimalUpdateView, UserEditView, UserAnimalDeleteView,
    CatalagoAnimalesListView, AdminEditView
)
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [

    path('', views.login, name='login'),

    # Rutas para animales
    path('animal/', AnimalListView.as_view(), name='animal-list'),
    path('animal/new/', AnimalCreateView.as_view(), name='animal-create'),
    path('animal/<int:pk>/edit/', AnimalUpdateView.as_view(), name='animal-update'),
    path('animal/<int:pk>/delete/', AnimalDeleteAjaxView.as_view(), name='animal-delete'),
    path('animal/edit/', AdminEditView.as_view(), name='admin-edit'),

    #Rutas para adoptantes
    path('adoptantes/', AdoptanteListView.as_view(), name='adoptante-list'),
    path('adoptantes/create/', AdoptanteCreateView.as_view(), name='adoptante-create'),
    path('adoptantes/<str:pk>/update/', AdoptanteUpdateView.as_view(), name='adoptante-update'),
    path('adoptantes/<str:pk>/delete/', AdoptanteDeleteAjaxView.as_view(), name='adoptante-delete'),

    #Rutas para adopciones
    path('adopciones/', AdopcionesListView.as_view(), name='adopciones-list'),
    path('adopciones/create/', AdopcionesCreateView.as_view(), name='adopcion-create'),
    path('adopciones/<int:pk>/delete/', AdopcionesDeleteView.as_view(), name='adopcion-delete'),

    #Rutas para voluntario
    path('voluntarios/', VoluntariosListView.as_view(), name='voluntarios-list'),
    path('voluntarios/<int:pk>/edit/', VoluntarioEditView.as_view(), name='voluntarios-update'),
    path('voluntarios/<int:pk>/delete/', VoluntarioDeleteView.as_view(), name='voluntarios-delete'),

    #Rutas para usuarios
    path('user/', UserAnimalesListView.as_view(), name='user'),
    path('user/agregar-animal/', UserAnimalCreateView.as_view(), name='agregar-animal'),
    path('user/update/<pk>/', UserAnimalUpdateView.as_view(), name='actualizar-animal'),
    path('user/edit/', UserEditView.as_view(), name='user-edit'),
    path('user/delete/<int:pk>/', UserAnimalDeleteView.as_view(), name='eliminar-animal'),

    #Ruta para catalogo
    path('catalago/', CatalagoAnimalesListView.as_view(), name='catalago-animales'),


    #Rutas de login

    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('redirec/',views.redirec, name='redirec')

    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
