import os
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404, render
from django.db.models import Q, Count
from .models import Animalesdb, Adoptantedb, Adopcionesdb,User
from .forms import AnimalesForm, AdoptanteForm, AdopcionesForm, UserForm, UserUpdateForm, AnimalesUpdateForm, AdoptanteUpdateForm, UserEditForm
from fpdf import FPDF
from datetime import datetime
from APP.conexion import *
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserRegisterForm, LoginForm
from django.contrib import messages
from .Pdf import *


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            if user.is_staff:  # O si utilizas otro campo para determinar si es admin
                return redirect('animal-list')  # Redirigir al admin
            else:
                return redirect('user')  # Redirigir al usuario normal

    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout(request):
    auth_logout(request)
    return redirect('login')  # Cambia 'login' por la vista de inicio de sesión

def redirec(request):
    return render(request,"./animales/animal_list.html")



#Views Animales
class AnimalListView(ListView):
    model = Animalesdb
    template_name = 'animales/animal_list.html'
    context_object_name = 'animales'

    def get_queryset(self):
        queryset = Animalesdb.objects.filter(status=False)
        search_query = self.request.GET.get('query')  # Búsqueda
        especie_filter = self.request.GET.get('especie')  # Filtro de especie (Perros, Gatos)
        genero_filter = self.request.GET.get('genero')  # Filtro de género (Machos, Hembras)
        esterilizado_filter = self.request.GET.get('esterilizado')  # Filtro de esterilización (Sí, No)
        order_by = self.request.GET.get('o')  # Ordenar por edad

        # Filtrar por búsqueda
        if search_query:
            queryset = queryset.filter(
                Q(id__icontains=search_query) |
                Q(nom__icontains=search_query) |
                Q(raza__icontains=search_query) |
                Q(fk_user__Cedula__icontains=search_query)
            )

        # Filtro por especie (Perros, Gatos, Todos)
        if especie_filter and especie_filter != "":  # Verificar que no sea vacío (Todos)
            queryset = queryset.filter(fk_esp__especie=especie_filter)

        # Filtro por género (Machos, Hembras, Todos)
        if genero_filter and genero_filter != "":  # Verificar que no sea vacío (Todos)
            queryset = queryset.filter(fk_gen__gen=genero_filter)

        # Filtro por esterilización (Sí, No, Todos)
        if esterilizado_filter and esterilizado_filter != "":  # Verificar que no sea vacío (Todos)
            if esterilizado_filter == 'Si':
                queryset = queryset.filter(fk_est__est='Si')
            elif esterilizado_filter == 'No':
                queryset = queryset.filter(fk_est__est='No')

        # Ordenar por edad si se solicita
        if order_by in ['Edad', '-Edad']:
            if order_by == 'Edad':
                queryset = queryset.order_by('edad')  # Orden ascendente
            elif order_by == '-Edad':
                queryset = queryset.order_by('-edad')  # Orden descendente

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Contar perros no adoptados
        context['cantidad_perros'] = Animalesdb.objects.filter(fk_esp__especie='Perro', status=False).count()
        # Contar gatos no adoptados
        context['cantidad_gatos'] = Animalesdb.objects.filter(fk_esp__especie='Gato', status=False).count()
        return context

class AnimalCreateView(CreateView):
    model = Animalesdb
    form_class = AnimalesForm
    template_name = 'animales/animal_form.html'
    success_url = reverse_lazy('animal-list')

    def form_valid(self, form):
        animal = form.save(commit=False)  # No guardar aún en la base de datos
        animal.status = False  # Asignar un valor predeterminado para 'status'
        animal.save()  # Guardar el animal en la base de datos

        return super().form_valid(form)

class AnimalUpdateView(UpdateView):
    model = Animalesdb
    form_class = AnimalesUpdateForm
    template_name = 'animales/animal_form.html'
    success_url = reverse_lazy('animal-list')

    def form_valid(self, form):
        animal = self.get_object()  # Obtener el objeto actual (animal)
        
        # Guardamos la foto actual del animal antes de actualizar
        old_photo = animal.photo

        # Verificar si se ha subido una nueva imagen
        if 'photo' in self.request.FILES:
            new_photo = form.cleaned_data.get('photo')
            
            # Si se ha subido una nueva imagen, eliminar la antigua si no es la predeterminada
            if old_photo and old_photo.name != "Animal_default.jpg":
                old_photo_path = old_photo.path
                response = super().form_valid(form)

                # Borrar la foto anterior si existe en el sistema de archivos
                if os.path.isfile(old_photo_path):
                    os.remove(old_photo_path)
                
                return response
        else:
            # Si no se sube una nueva imagen, mantener la imagen antigua
            form.instance.photo = old_photo
        
        return super().form_valid(form)
    

class AnimalDeleteAjaxView(DeleteView):
    model = Animalesdb
    success_url = reverse_lazy('animal-list')  # Redirige a la lista de animales tras la eliminación

    def post(self, request, *args, **kwargs):
        # Obtener el objeto del animal
        self.object = self.get_object()

        # Verificar si el animal tiene una imagen y eliminarla
        if self.object.photo and os.path.isfile(self.object.photo.path):
            os.remove(self.object.photo.path)

        # Eliminar el objeto del animal
        self.object.delete()

        # Responder con JSON indicando éxito y la URL de redirección
        response_data = {
            'success': True,
            'redirect_url': str(self.success_url)
        }
        return JsonResponse(response_data)
    
#Views Adoptantes

class AdoptanteListView(ListView):
    model = Adoptantedb
    template_name = 'adoptantes/adoptante_list.html'  # Ruta a la plantilla
    context_object_name = 'object_list'  # Define el nombre del contexto

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('search')  # Obtén el valor del parámetro de búsqueda
        if query:
            # Filtra por nombre o cédula
            queryset = queryset.filter(
                Q(name__icontains=query) | 
                Q(ced__icontains=query) |
                Q(ape__icontains=query)
            )
        return queryset

class AdoptanteCreateView(CreateView):
    model = Adoptantedb
    form_class = AdoptanteForm
    template_name = 'adoptantes/adoptante_form.html'
    success_url = reverse_lazy('adoptante-list')

class AdoptanteUpdateView(UpdateView):
    model = Adoptantedb
    form_class = AdoptanteUpdateForm
    template_name = 'adoptantes/adoptante_form.html'
    success_url = reverse_lazy('adoptante-list')

class AdoptanteUpdateView(UpdateView):
    model = Adoptantedb
    form_class = AdoptanteUpdateForm
    template_name = 'adoptantes/adoptante_form.html'
    success_url = reverse_lazy('adoptante-list')

class AdoptanteUpdateView(UpdateView):
    model = Adoptantedb
    form_class = AdoptanteUpdateForm
    template_name = 'adoptantes/adoptante_form.html'
    success_url = reverse_lazy('adoptante-list')

    def form_valid(self, form):
        adoptante = self.get_object()  # Obtener el adoptante actual
        
        # Guardamos la foto actual del adoptante antes de actualizar
        old_photo = adoptante.photo

        # Verificar si se ha subido una nueva imagen
        if 'photo' in self.request.FILES:
            new_photo = form.cleaned_data.get('photo')
            
            # Si hay una nueva imagen, eliminamos la antigua si no es la predeterminada
            if old_photo and old_photo.name != "Adoptante_default.png":
                old_photo_path = old_photo.path
                response = super().form_valid(form)
                
                # Borrar la foto anterior si existe en el sistema de archivos
                if os.path.isfile(old_photo_path):
                    os.remove(old_photo_path)
                
                return response
        else:
            # Si no se sube una nueva imagen, mantenemos la imagen antigua
            form.instance.photo = old_photo
        
        return super().form_valid(form)

class AdoptanteDeleteAjaxView(View):
    def post(self, request, *args, **kwargs):
        # Obtener el adoptante por su pk
        adoptante = get_object_or_404(Adoptantedb, pk=self.kwargs['pk'])

        # Verificar si el adoptante tiene adopciones asociadas
        adopciones_existentes = Adopcionesdb.objects.filter(Adoptante=adoptante).exists()

        if adopciones_existentes:
            # Devolver un error si hay adopciones asociadas
            return JsonResponse({
                'success': False,
                'error': 'No se puede eliminar el adoptante porque tiene adopciones asociadas.'
            })

        # Verificar si el adoptante tiene una foto personalizada (diferente de la foto por defecto)
        if adoptante.photo and adoptante.photo.name != "Adoptante_default.png" and os.path.isfile(adoptante.photo.path):
            os.remove(adoptante.photo.path)

        # Eliminar al adoptante
        adoptante.delete()

        return JsonResponse({
            'success': True,
            'redirect_url': reverse('adoptante-list')
        })
    
#Views Adopciones

class AdopcionesListView(ListView):
    model = Adopcionesdb
    template_name = 'adopciones/adopciones_list.html'
    context_object_name = 'adopciones'

    def get_queryset(self):
        queryset = Adopcionesdb.objects.all().select_related('Animal', 'Adoptante')  # Relaciona con Animal y Adoptante
        search_query = self.request.GET.get('query')  # Captura el término de búsqueda
        especie_filter = self.request.GET.get('especie')  # Filtro de especie (Perros, Gatos)
        genero_filter = self.request.GET.get('genero')  # Filtro de género (Machos, Hembras)
        esterilizado_filter = self.request.GET.get('esterilizado')  # Filtro de esterilización (Sí, No)
        order_by = self.request.GET.get('o')  # Ordenar por edad

        # Filtrar según el término de búsqueda
        if search_query:
            queryset = queryset.filter(
                Q(Animal__nom__icontains=search_query) |  # Filtra por el nombre del animal
                Q(Adoptante__name__icontains=search_query) |  # Filtra por el nombre del adoptante
                Q(Adoptante__ape__icontains=search_query) |
                Q(Adoptante__ced__icontains=search_query) |  # Filtra por la cédula del adoptante
                Q(Animal__raza__icontains=search_query) |  # Filtra por la raza del animal
                Q(id__icontains=search_query)  # Filtra por el ID de la adopción
            )

        # Filtro por especie (Perros, Gatos, Todos)
        if especie_filter and especie_filter != "":  # Verificar que no sea vacío (Todos)
            queryset = queryset.filter(Animal__fk_esp__especie=especie_filter)

        # Filtro por género (Machos, Hembras, Todos)
        if genero_filter and genero_filter != "":  # Verificar que no sea vacío (Todos)
            queryset = queryset.filter(Animal__fk_gen__gen=genero_filter)

        # Filtro por esterilización (Sí, No, Todos)
        if esterilizado_filter and esterilizado_filter != "":  # Verificar que no sea vacío (Todos)
            if esterilizado_filter == 'Si':
                queryset = queryset.filter(Animal__fk_est__est='Si')
            elif esterilizado_filter == 'No':
                queryset = queryset.filter(Animal__fk_est__est='No')

        # Ordenar por edad si se solicita
        if order_by in ['Edad', '-Edad']:
            if order_by == 'Edad':
                queryset = queryset.order_by('Animal__edad')  # Orden ascendente
            elif order_by == '-Edad':
                queryset = queryset.order_by('-Animal__edad')  # Orden descendente

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('query', '')

        # Contar adopciones de perros y gatos
        context['cantidad_perros_adoptados'] = Adopcionesdb.objects.filter(Animal__fk_esp__especie='Perro').count()
        context['cantidad_gatos_adoptados'] = Adopcionesdb.objects.filter(Animal__fk_esp__especie='Gato').count()
        return context
    
class AdopcionesCreateView(CreateView):
    model = Adopcionesdb
    form_class = AdopcionesForm
    template_name = 'adopciones/adopciones_form.html'
    success_url = reverse_lazy('adopciones-list')

    def form_valid(self, form):
        adopcion = form.save(commit=False)
        animal = adopcion.Animal  # Obtener el animal relacionado
        animal.status = True  # Cambiar el estado del animal a adoptado
        animal.fk_user_id = 1
        animal.save()  # Guardar el cambio en el modelo Animal
        return super().form_valid(form)

class AdopcionesDeleteView(DeleteView):
    model = Adopcionesdb
    template_name = 'adopciones/adopciones_confirm_delete.html'
    success_url = reverse_lazy('adopciones-list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        animal = self.object.Animal  # Obtener el animal relacionado
        animal.status = False  # Cambiar el estado del animal a disponible
        animal.save()  # Guardar el cambio en el modelo Animal
        self.object.delete()  # Eliminar la adopción

        response_data = {
            'success': True,
            'redirect_url': str(self.success_url)
        }
        return JsonResponse(response_data)  # Devolver una respuesta JSON

#Vista Voluntarios

User = get_user_model() 

class VoluntariosListView(ListView):
    model = User
    template_name = 'resguardo/voluntarios_list.html'
    context_object_name = 'voluntarios'

    def get_queryset(self):
        # Obtener el queryset base con conteo de perros y gatos, excluyendo los adoptados
        queryset = User.objects.annotate(
            perros_count=Count('animalesdb', filter=Q(animalesdb__fk_esp__especie='Perro') & Q(animalesdb__adopcionesdb__isnull=True)),  # Solo perros no adoptados
            gatos_count=Count('animalesdb', filter=Q(animalesdb__fk_esp__especie='Gato') & Q(animalesdb__adopcionesdb__isnull=True))   # Solo gatos no adoptados
        )
        
        # Obtener el término de búsqueda
        search_query = self.request.GET.get('query')

        # Filtrar el queryset según el término de búsqueda
        if search_query:
            queryset = queryset.filter(
                Q(first_name__icontains=search_query) |  # Busca por el nombre
                Q(last_name__icontains=search_query) |  # Busca por el apellido
                Q(Cedula__icontains=search_query)  # Busca por la cédula
            )

        return queryset
    
class VoluntarioEditView(UpdateView):
    model = User
    form_class = UserEditForm
    template_name = 'resguardo/voluntario_edit.html'  
    success_url = reverse_lazy('voluntarios-list')


    def form_valid(self, form):
        user = self.get_object()  # Obtener el objeto actual (usuario)

        # Guardar la foto actual del usuario antes de actualizar
        old_photo = user.photo
        
        response = super().form_valid(form)

        # Verificar si se ha subido una nueva imagen
        if 'photo' in self.request.FILES:
            new_photo = form.cleaned_data.get('photo')

            # Si se ha subido una nueva imagen y la antigua no es la predeterminada, eliminar la anterior
            if old_photo and old_photo.name != "User_default.jpg":
                old_photo_path = old_photo.path
                
                # Borrar la foto anterior si existe en el sistema de archivos
                if os.path.isfile(old_photo_path):
                    os.remove(old_photo_path)

        return response
    
class VoluntarioDeleteView(DeleteView):
    model = User
    success_url = reverse_lazy('voluntarios-list')  # Redirigir a la lista de voluntarios después de la eliminación

    def post(self, request, pk, *args, **kwargs):
        # Obtener al voluntario por su pk
        voluntario = get_object_or_404(User, pk=pk)

        # Verificar si tiene animales asociados
        if voluntario.animalesdb_set.exists():
            return JsonResponse({
                'success': False,
                'error': 'Este voluntario no puede ser eliminado porque tiene animales asociados.'
            })

        # Verificar si el voluntario tiene una foto personalizada (diferente de la foto por defecto)
        if voluntario.photo and voluntario.photo.name != "User_default.jpg" and os.path.isfile(voluntario.photo.path):
            os.remove(voluntario.photo.path)

        # Eliminar al voluntario
        voluntario.delete()

        return JsonResponse({'success': True})

#Vista Usuarios

class UserAnimalesListView(LoginRequiredMixin, ListView):
    model = Animalesdb
    template_name = 'user/mi_refugio.html'  # Aquí usaremos una plantilla específica para el usuario normal
    context_object_name = 'animales'
    
    # Filtrar los animales asociados al usuario autenticado
    def get_queryset(self):
        # Filtrar animales por el usuario actual
        queryset = Animalesdb.objects.filter(fk_user=self.request.user, status=False)
        search_query = self.request.GET.get('query')  # Captura el término de búsqueda
        especie_filter = self.request.GET.get('especie')  # Filtro de especie (Perros, Gatos)
        genero_filter = self.request.GET.get('genero')  # Filtro de género (Machos, Hembras)
        esterilizado_filter = self.request.GET.get('esterilizado')  # Filtro de esterilización (Sí, No)
        order_by = self.request.GET.get('o')  # Ordenar por edad

        if search_query:
            queryset = queryset.filter(
                Q(id__icontains=search_query) |
                Q(nom__icontains=search_query) |
                Q(raza__icontains=search_query)
            )

        # Filtro por especie (Perros, Gatos, Todos)
        if especie_filter and especie_filter != "":  # Verificar que no sea vacío (Todos)
            queryset = queryset.filter(fk_esp__especie=especie_filter)

        # Filtro por género (Machos, Hembras, Todos)
        if genero_filter and genero_filter != "":  # Verificar que no sea vacío (Todos)
            queryset = queryset.filter(fk_gen__gen=genero_filter)

        # Filtro por esterilización (Sí, No, Todos)
        if esterilizado_filter and esterilizado_filter != "":  # Verificar que no sea vacío (Todos)
            if esterilizado_filter == 'Si':
                queryset = queryset.filter(fk_est__est='Si')
            elif esterilizado_filter == 'No':
                queryset = queryset.filter(fk_est__est='No')

        # Ordenar por edad si se solicita
        if order_by in ['Edad', '-Edad']:
            if order_by == 'Edad':
                queryset = queryset.order_by('edad')  # Orden ascendente
            elif order_by == '-Edad':
                queryset = queryset.order_by('-edad')  # Orden descendente

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Contar perros y gatos del usuario actual
        context['cantidad_perros'] = Animalesdb.objects.filter(fk_user=self.request.user, fk_esp__especie='Perro').count()
        context['cantidad_gatos'] = Animalesdb.objects.filter(fk_user=self.request.user, fk_esp__especie='Gato').count()
        return context
    
    
class UserAnimalCreateView(LoginRequiredMixin, CreateView):
    model = Animalesdb
    form_class = UserForm
    template_name = 'user/user_animal_form.html'  
    success_url = reverse_lazy('user')  

    def form_valid(self, form):
        form.instance.fk_user = self.request.user  # Asigna el usuario actual
        return super().form_valid(form)
    
class UserAnimalUpdateView(LoginRequiredMixin, UpdateView):
    model = Animalesdb
    form_class = UserUpdateForm
    template_name = 'user/user_animal_form.html'
    success_url = reverse_lazy('user')  

    def get_queryset(self):
        # Asegurarse de que solo el usuario que creó el animal pueda actualizarlo
        return Animalesdb.objects.filter(fk_user=self.request.user)
    
    def form_valid(self, form):
       
        animal_instance = self.get_object()  # Obtén la instancia del animal que se está editando
       
        form.instance.fk_user = animal_instance.fk_user  # Asegúrate de que el usuario no se cambie
        return super().form_valid(form)

class UserEditView(UpdateView):
    model = User
    form_class = UserEditForm
    template_name = 'user/user_edit.html'
    success_url = reverse_lazy('login')

    def get_object(self, queryset=None):
        return self.request.user  # Edita el usuario actual
    
    def form_valid(self, form):
        user = self.get_object()  # Obtener el objeto actual (usuario)

        # Guardar la foto actual del usuario antes de actualizar
        old_photo = user.photo
        
        # Llamar a super().form_valid() para guardar los cambios en el formulario
        response = super().form_valid(form)

        # Verificar si se ha subido una nueva imagen
        if 'photo' in self.request.FILES:
            new_photo = form.cleaned_data.get('photo')
            user.photo = new_photo  # Asignar la nueva foto al usuario
            user.save()  # Guardar el usuario con la nueva foto

            # Si se ha subido una nueva imagen y la antigua no es la predeterminada, eliminar la anterior
            if old_photo and old_photo.name != "User_default.jpg":
                old_photo_path = old_photo.path
                
                # Borrar la foto anterior si existe en el sistema de archivos
                if os.path.isfile(old_photo_path):
                    os.remove(old_photo_path)

        return response

    def form_invalid(self, form):
        # Si el formulario no es válido, devuelve el mismo template con errores
        return super().form_invalid(form)
    
class AdminEditView(UpdateView):
    model = User
    form_class = UserEditForm
    template_name = 'animales/admin_edit.html'  
    success_url = reverse_lazy('login')

    def get_object(self, queryset=None):
        return self.request.user  # Edita el usuario actual
    
    def form_valid(self, form):
        user = self.get_object()  # Obtener el objeto actual (usuario)

        # Guardar la foto actual del usuario antes de actualizar
        old_photo = user.photo
        
        # Llamar a super().form_valid() para guardar los cambios en el formulario
        response = super().form_valid(form)

        # Verificar si se ha subido una nueva imagen
        if 'photo' in self.request.FILES:
            new_photo = form.cleaned_data.get('photo')
            user.photo = new_photo  # Asignar la nueva foto al usuario
            user.save()  # Guardar el usuario con la nueva foto

            # Si se ha subido una nueva imagen y la antigua no es la predeterminada, eliminar la anterior
            if old_photo and old_photo.name != "User_default.jpg":
                old_photo_path = old_photo.path
                
                # Borrar la foto anterior si existe en el sistema de archivos
                if os.path.isfile(old_photo_path):
                    os.remove(old_photo_path)

        return response

    def form_invalid(self, form):
        # Si el formulario no es válido, devuelve el mismo template con errores
        return super().form_invalid(form)

class UserAnimalDeleteView(LoginRequiredMixin, DeleteView):
    model = Animalesdb
    success_url = reverse_lazy('user')  # Redirige a la lista de animales tras la eliminación

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        response_data = {
            'success': True,
            'redirect_url': self.success_url
        }
        return JsonResponse(response_data)

class CatalagoAnimalesListView(ListView):
    model = Animalesdb
    template_name = 'catalago/catalago.html'  # Cambia esto al nombre de tu plantilla
    context_object_name = 'animales'  # Nombre del contexto que usaremos en la plantilla

    def get_queryset(self):
        # Filtra los animales que están disponibles (status=False) y que no son la imagen por defecto
        queryset = Animalesdb.objects.filter(
            status=False
        ).exclude(
            photo__in=['Animal_default.png', 'Animal_default.jpg']
        ).filter(photo__isnull=False)

        # Captura los parámetros de la URL para la búsqueda y filtros
        search_query = self.request.GET.get('query')  # Término de búsqueda
        especie_filter = self.request.GET.get('especie')  # Filtro de especie (Perros, Gatos)
        genero_filter = self.request.GET.get('genero')  # Filtro de género (Machos, Hembras)
        esterilizado_filter = self.request.GET.get('esterilizado')  # Filtro de esterilización (Sí, No)
        tamaño_filter = self.request.GET.get('tamaño')  # Filtro de tamaño (Pequeño, Grande)
        order_by = self.request.GET.get('o')  # Ordenar por edad

        # Filtro por búsqueda
        if search_query:
            queryset = queryset.filter(
                Q(raza__icontains=search_query)
            )

        # Filtro por especie (Perros, Gatos, Todos)
        if especie_filter and especie_filter != "":  # Verificar que no sea vacío (Todos)
            queryset = queryset.filter(fk_esp__especie=especie_filter)

        # Filtro por género (Machos, Hembras, Todos)
        if genero_filter and genero_filter != "":  # Verificar que no sea vacío (Todos)
            queryset = queryset.filter(fk_gen__gen=genero_filter)

        # Filtro por esterilización (Sí, No, Todos)
        if esterilizado_filter and esterilizado_filter != "":  # Verificar que no sea vacío (Todos)
            if esterilizado_filter == 'Si':
                queryset = queryset.filter(fk_est__est='Si')
            elif esterilizado_filter == 'No':
                queryset = queryset.filter(fk_est__est='No')

        # Filtro por tamaño (Pequeño, Grande, Todos)
        if tamaño_filter and tamaño_filter != "":  # Verificar que no sea vacío (Todos)
            queryset = queryset.filter(fk_tam__tamaño=tamaño_filter)

        # Ordenar por edad si se solicita
        if order_by in ['Edad', '-Edad']:
            if order_by == 'Edad':
                queryset = queryset.order_by('edad')  # Orden ascendente
            elif order_by == '-Edad':
                queryset = queryset.order_by('-edad')  # Orden descendente

        return queryset



#Declaracion de las Fechas Los archivos que cambie fueron Views EL INDEX y urls
fecha_actual = datetime.now()


# Create your views here.
def IndexView(request):
    return render(request,'index.html')

def generar_pdf_resguardo(request):
    report_title = "Reporte General de Animales" # modificacion dinamica del header guia por cada variable
    

    cantidad_perros=("""
        select COUNT(*)
        FROM animales 
        WHERE fk_esp_id = 1 AND status = 0
        """)

    perros=ejecutar_consulta(cantidad_perros)

    for i in perros:
         for num in i:
             p=num

    cantidad_gatos=("""
        select COUNT(*)
        FROM animales
        WHERE fk_esp_id = 2 AND status = 0
        """)
    
    gatos=ejecutar_consulta(cantidad_gatos)

    for i in gatos:
        for num in i:
            g = num


    # variable para hacer multipdf la fecha y hora como una cadena (por ejemplo, "2024-07-25_09-30-15")
    
    nombre_archivo = fecha_actual.strftime("Resguardo_%Y-%m-%d_%H-%M") + ".pdf"

    # Cambiar la orientación a horizontal, uso de las variables declaradas para el header
    # Ejecutar la clase
    pdf = PDF_animales( report_title=report_title,contador_perro=p,contador_gato=g, orientation='L', format='letter') 

    consulta=("""
        SELECT M.id, M.nom , M.edad,h.especie, M.raza,e.est ,t.tamaño,g.gen,V.Cedula
        FROM animales AS M
        INNER JOIN app_user AS V ON M.fk_user_id = V.id
        INNER JOIN tipo AS h ON M.fk_esp_id = h.id           
        INNER JOIN esterilizacion AS e ON M.fk_est_id = e.id
        INNER JOIN tamaño AS t ON M.fk_tam_id = t.id
        INNER JOIN generos AS g ON M.fk_gen_id= g.id
        WHERE M.status = 0
        ORDER BY M.id ASC
        """)

    datos= ejecutar_consulta(consulta)
    
    pdf_resguardo(pdf,datos)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{nombre_archivo}"'
    pdf.output(dest='S').encode('latin1')
    response.write(pdf.output(dest='S').encode('latin1'))
    return response

## PDF DE Voluntarios
def generar_pdf_voluntarios(request):
    report_title = "Reporte Voluntarios"
    
    # variable para hacer multipdf la fecha y hora como una cadena (por ejemplo, "2024-07-25_09-30-15")
    nombre_archivo = fecha_actual.strftime("Voluntarios_%Y-%m-%d_%H-%M") + ".pdf"


    # Ejecutar la clase
    pdf = PDF( report_title=report_title, orientation='L', format='letter')  # Cambiar la orientación a horizontal
    consulta=("""
        SELECT  Cedula, first_name,last_name, Telefono,email FROM app_user
        """)

    datos= ejecutar_consulta(consulta)

    pdf_voluntarios(pdf,datos)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{nombre_archivo}"'
    pdf.output(dest='S').encode('latin1')
    response.write(pdf.output(dest='S').encode('latin1'))
    return response

def generar_pdf_propio(request,user_id):
    
    Usuario= User.objects.get(id=user_id)

    report_title=(f'Reporte Personal {Usuario.first_name}, {Usuario.last_name}') #colocar las variables que identifican al voluntario
    cedula = (f"C.I:{Usuario.Cedula}") # y su cedula
    # variable para hacer multipdf la fecha y hora como una cadena (por ejemplo, "2024-07-25_09-30-15")
    nombre_archivo = fecha_actual.strftime("Reporte General _%Y-%m-%d_%H-%M") + ".pdf"

    a=(Usuario.Cedula,)

    cantidad_perros=("""
        SELECT COUNT(*) 
        FROM animales AS M 
        INNER JOIN app_user AS V ON M.fk_user_id = V.id
        WHERE fk_esp_id = 1 AND V.Cedula = %s AND STATUS = 0
        """)

    perros=consulta_pdf_propio(cantidad_perros,a)

    for i in perros:
         for num in i:
             p=num

    cantidad_gatos=("""
        SELECT COUNT(*) 
        FROM animales AS M 
        INNER JOIN app_user AS V ON M.fk_user_id = V.id
        WHERE fk_esp_id = 2 AND V.Cedula = %s AND STATUS = 0
        """)
    
    gatos=consulta_pdf_propio(cantidad_gatos,a)

    for i in gatos:
        for num in i:
            g = num

    

    # Ejecutar la clase
    pdf = PDF_animales( report_title=report_title, rif=cedula, contador_perro=p,contador_gato=g, orientation='L', format='letter')  # Cambiar la orientación a horizontal

    
    consulta=("""
        SELECT M.id, M.nom , M.edad,h.especie, M.raza,e.est ,t.tamaño,g.gen
        FROM animales AS M
        INNER JOIN app_user AS V ON M.fk_user_id = V.id
        INNER JOIN tipo AS h ON M.fk_esp_id = h.id           
        INNER JOIN esterilizacion AS e ON M.fk_est_id = e.id
        INNER JOIN tamaño AS t ON M.fk_tam_id = t.id
        INNER JOIN generos AS g ON M.fk_gen_id= g.id
        WHERE V.Cedula = %s AND M.status = 0
        """)

    datos= consulta_pdf_propio(consulta,a)
    
    pdf_propio(pdf,datos)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{nombre_archivo}"'
    pdf.output(dest='S').encode('latin1')
    response.write(pdf.output(dest='S').encode('latin1'))
    return response

def generar_pdf_adopciones(request):
    report_title = "Reporte de Adopciones"
    rif = "Rif: 12809142"
    
    cantidad_perros=("""
        select COUNT(*)
        FROM adopciones AS a
        INNER JOIN animales AS M ON M.id = a.Animal_id
        WHERE M.fk_esp_id = 1
        """)

    perros=ejecutar_consulta(cantidad_perros)

    for i in perros:
         for num in i:
             p=num

    cantidad_gatos=("""
        select COUNT(*)
        FROM adopciones AS a
        INNER JOIN animales AS M ON M.id = a.Animal_id
        WHERE M.fk_esp_id = 2
        """)
    
    gatos=ejecutar_consulta(cantidad_gatos)

    for i in gatos:
        for num in i:
            g = num


    # Obtiene la fecha y hora actuales
    fecha_actual = datetime.now()

    # variable para hacer multipdf la fecha y hora como una cadena (por ejemplo, "2024-07-25_09-30-15")
    nombre_archivo = fecha_actual.strftime("Adopciones_%Y-%m-%d_%H-%M") + ".pdf"
    

    # Ejecutar la clase
    pdf = PDF_animales( report_title=report_title, rif=rif,contador_perro=p ,contador_gato=g,orientation='L', format='letter')  # Cambiar la orientación a horizontal

    consulta=("""
        SELECT M.id, M.nom,M.edad,h.especie,g.gen,a.ced,a.name,a.ape,a.tlf,r.Fecha
        FROM adopciones AS r
        INNER JOIN adoptantes AS a ON a.ced = r.Adoptante_id 
        INNER JOIN animales AS M ON M.id = r.Animal_id
        INNER JOIN tipo AS h ON M.fk_esp_id = h.id           
        INNER JOIN esterilizacion AS e ON M.fk_est_id = e.id
        INNER JOIN tamaño AS t ON M.fk_tam_id = t.id
        INNER JOIN generos AS g ON M.fk_gen_id= g.id
        """)

    datos= ejecutar_consulta(consulta)

    pdf_adopciones(pdf,datos)


    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{nombre_archivo}"'
    pdf.output(dest='S').encode('latin1')
    response.write(pdf.output(dest='S').encode('latin1'))
    return response

def generar_pdf_adoptantes(request):
    report_title = "Reporte de Adoptantes"
    
    # variable para hacer multipdf la fecha y hora como una cadena (por ejemplo, "2024-07-25_09-30-15")
    nombre_archivo = fecha_actual.strftime("Adoptantes_%Y-%m-%d_%H-%M") + ".pdf"

    # Ejecutar la clase
    pdf = PDF( report_title=report_title, orientation='L', format='letter')  # Cambiar la orientación a horizontal

    consulta=("""
        SELECT ced,name,ape,tlf FROM adoptantes
        """)

    datos= ejecutar_consulta(consulta)

    pdf_adoptantes(pdf,datos)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{nombre_archivo}"'
    pdf.output(dest='S').encode('latin1')
    response.write(pdf.output(dest='S').encode('latin1'))
    return response

# Pdf de las fichas de adopciones
def generar_pdf_ficha(request,adopcion_id):
    # Declaracion de los animales, adoptantes y la adopcion como objetos
    adopcion= Adopcionesdb.objects.get(id=adopcion_id)

    # Ejecutar la clase
    
    nombre_archivo= (f"Ficha de Compromiso {adopcion.Animal.nom}") + (".pdf")
    pdf = PDF_Ficha(format='letter')  # Cambiar la orientación a horizontal
    
    pdf_ficha(pdf,adopcion)


    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{nombre_archivo}"'
    pdf.output(dest='S').encode('latin1')
    response.write(pdf.output(dest='S').encode('latin1'))
    return response

#Pdf de los animales sin esterilizar
def generar_pdf_sin_esterilizar(request):
    report_title=(f'Reporte Animales sin esterilizar') #colocar las variables que identifican al voluntario
     # y su cedula
    # variable para hacer multipdf la fecha y hora como una cadena (por ejemplo, "2024-07-25_09-30-15")
    nombre_archivo = fecha_actual.strftime("Reporte de animales sin esterilizar _%Y-%m-%d_%H-%M") + ".pdf"

    consulta=("""
        SELECT M.id, M.nom , M.edad,h.especie, M.raza,e.est ,t.tamaño,g.gen
        FROM animales AS M
        INNER JOIN app_user AS V ON M.fk_user_id = V.id
        INNER JOIN tipo AS h ON M.fk_esp_id = h.id           
        INNER JOIN esterilizacion AS e ON M.fk_est_id = e.id
        INNER JOIN tamaño AS t ON M.fk_tam_id = t.id
        INNER JOIN generos AS g ON M.fk_gen_id= g.id
        WHERE e.est= "No" AND status = 0
        """)

    datos= ejecutar_consulta(consulta)

    pdf = PDF( report_title=report_title, orientation='L', format='letter')  # Cambiar la orientación a horizontal

    pdf_sin_esterilizar(pdf,datos)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{nombre_archivo}"'
    pdf.output(dest='S').encode('latin1')
    response.write(pdf.output(dest='S').encode('latin1'))
    return response
