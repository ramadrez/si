from django import forms
from .models import Animalesdb, Adoptantedb, Adopcionesdb, User
import datetime  
import re  
from django.core.exceptions import ValidationError  
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile 
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.contrib.auth.forms import AuthenticationForm
from django.forms import NumberInput


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(
        label='Nombre de Usuario',
        max_length=10,  # Establece el límite de caracteres aquí
        widget=forms.TextInput(attrs={
            'class': 'form-control m-2 input-form',
            'placeholder': 'Ingresar Nombre de Usuario',
            'aria-label': 'Nombre de Usuario',
            'required': True
        })
    )
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control m-2 input-form',
            'placeholder': 'Ingresa tu email',
            'aria-label': 'Email',
            'required': True
        })
    )
    Cedula = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control m-2 input-form',
            'placeholder': 'Ingresa tu cédula',
            'aria-label': 'Cédula'
        })
    )
    Telefono = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control m-2 input-form',
            'placeholder': 'Ingresa tu teléfono',
            'aria-label': 'Teléfono'
        })
    )
    photo = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control m-2 input-form',
            'aria-label': 'Foto'
        })
    )
    first_name = forms.CharField(
        max_length=10,
        required=True,
        label="Nombre",
        widget=forms.TextInput(attrs={
            'class': 'form-control m-2 input-form',
            'placeholder': 'Ingresa tu nombre',
            'aria-label': 'Nombre',
            'required': True
        })
    )
    last_name = forms.CharField(
        max_length=10,
        required=True,
        label="Apellido",
        widget=forms.TextInput(attrs={
            'class': 'form-control m-2 input-form',
            'placeholder': 'Ingresa tu apellido',
            'aria-label': 'Apellido',
            'required': True
        })
    )

    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control m-2 input-form',
            'placeholder': 'Ingresa tu contraseña',
            'aria-label': 'Contraseña',
            'required': True
        })
    )
    password2 = forms.CharField(
        label='Confirmar Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control m-2 input-form',
            'placeholder': 'Confirma tu contraseña',
            'aria-label': 'Confirmar Contraseña',
            'required': True
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email','first_name', 'last_name', 'Cedula', 'Telefono', 'photo', 'password1', 'password2']

# Validar que el username sea único
    def clean_username(self):
        username = self.cleaned_data.get('username')

        # Validar que el username contenga solo letras y tenga un máximo de 15 caracteres
        if not re.match(r'^[a-zA-Z]{1,10}$', username):
            raise forms.ValidationError('El nombre de usuario solo puede contener letras y debe tener un máximo de 10 caracteres.')

        # Verificar si el nombre de usuario ya está en uso
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('El nombre de usuario ya está en uso. Por favor, elige uno diferente.')

        return username


# Validar que el email sea único
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Este correo electrónico ya está registrado.")
        return email

    # Validar que la cédula sea única
    def clean_Cedula(self):
        Cedula = self.cleaned_data.get('Cedula')

        # Verificar si la cédula ya está registrada
        if Cedula and User.objects.filter(Cedula=Cedula).exists():
            raise ValidationError("Esta cédula ya está registrada.")

        # Expresión regular para cédula venezolana (V o E seguida de 7 u 8 dígitos)
        venezolana_regex = r'^[V]-?\d{7,8}$'

        # Expresión regular para cédula colombiana (solo dígitos de 6 a 10)
        colombiana_regex = r'^[C]-?\d{9,10}$'

        # Verificar si coincide con cédula venezolana
        if re.match(venezolana_regex, Cedula):
            return Cedula

        # Verificar si coincide con cédula colombiana
        elif re.match(colombiana_regex, Cedula):
            return Cedula

        # Si no coincide con ninguno, lanzar un error de validación
        raise ValidationError('La cédula debe ser válida para venezolanos (V seguido de 7-8 dígitos) o colombianos (C seguido de 9-10 dígitos).')

    ## Validación del teléfono
    def clean_Telefono(self):
        Telefono = self.cleaned_data.get('Telefono')

        # Verificar la longitud mínima del teléfono
        if Telefono and len(Telefono) < 10:
            raise forms.ValidationError("El teléfono debe tener al menos 10 dígitos.")

        # Validar formatos de teléfono
        colombian_pattern = r'^(57)?(3\d{2})\d{7}$'
        venezuelan_pattern = r'^(58|0)?(412|416|414|426|424)\d{7}$'

        # Validación de números venezolanos
        if re.match(venezuelan_pattern, Telefono):
            # Si empieza con "0", lo reemplazamos con "+58"
            if Telefono.startswith('0'):
                Telefono = '58' + Telefono[1:]
            return Telefono

        # Validación de números colombianos
        if re.match(colombian_pattern, Telefono):
            if not Telefono.startswith('57'):
                # Si no empieza con "+57", lo añadimos
                Telefono = '57' + Telefono
            return Telefono

        # Si el número no es válido, lanzamos un error
        raise forms.ValidationError("El número de teléfono debe ser un número válido de Venezuela o Colombia.")
    
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not re.match("^[A-Za-záéíóúÁÉÍÓÚñÑ]+$", first_name):
            raise forms.ValidationError("El nombre solo debe contener letras.")
        return first_name
    
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not re.match("^[A-Za-záéíóúÁÉÍÓÚñÑ]+$", last_name):
            raise forms.ValidationError("El apellido solo debe contener letras.")
        return last_name
    
    # Validar que las contraseñas coinciden y otras validaciones generales
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Las contraseñas no coinciden.")

        if password1 and len(password1) < 8:
            raise ValidationError("La contraseña debe tener al menos 8 caracteres.")

        return cleaned_data

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Nombre de Usuario',
        widget=forms.TextInput(attrs={
            'class': 'form-control m-2 input-form',
            'placeholder': 'Ingresar Nombre de Usuario',
            'aria-label': 'Identificador Animal',
            'autofocus': True,
            'required': True
        })
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control m-2 input-form',
            'placeholder': 'Ingresar Contraseña'
        })
    )

#toque aqui formularios animales
class AnimalesForm(forms.ModelForm):
    
    class Meta:
        model = Animalesdb
        exclude = ['status']
        fields = ['photo', 'nom', 'edad', 'fk_esp', 'raza', 'fk_est', 'fk_tam', 'fk_gen', 'fk_user']
        widgets = {
            'edad': forms.DateInput(attrs={
                'class': 'form-control m-2 input-form',
                'type': 'date',
                'aria-label': 'Edad'
            }),
            'photo': forms.FileInput(attrs={
                'class': 'form-control m-2 input-form',
                'aria-label': 'Foto'
            }),
            'nom': forms.TextInput(attrs={
                'class': 'form-control m-2 input-form',
                'placeholder': 'Nombre del Animal',
                'aria-label': 'Nombre'
            }),
            'fk_esp': forms.Select(attrs={
                'class': 'form-control m-2 input-form custom-select',
                'aria-label': 'Especie'
            }),
            'raza': forms.TextInput(attrs={
                'class': 'form-control m-2 input-form',
                'placeholder': 'Raza del Animal',
                'aria-label': 'Raza'
            }),
            'fk_est': forms.Select(attrs={
                'class': 'form-control m-2 input-form custom-select',
                'aria-label': 'Estado'
            }),
            'fk_tam': forms.Select(attrs={
                'class': 'form-control m-2 input-form custom-select',
                'aria-label': 'Tamaño'
            }),
            'fk_gen': forms.Select(attrs={
                'class': 'form-control m-2 input-form custom-select',
                'aria-label': 'Género'
            }),
            'fk_user': forms.Select(attrs={
                'class': 'form-control m-2 input-form custom-select',
                'aria-label': 'cuidador'
            }),
        }
#formularios animales

    def __init__(self, *args, **kwargs):
        super(AnimalesForm, self).__init__(*args, **kwargs)
        self.fields['fk_user'].queryset = User.objects.all().order_by('Cedula')
        self.fields['fk_user'].label_from_instance = lambda obj: f'{obj.Cedula} - {obj.get_full_name()}'

    def clean_nom(self):
        nom = self.cleaned_data.get('nom')
        if len(nom) > 10:
            raise forms.ValidationError("El nombre no puede tener más de 10 caracteres.")
        if not re.match(r'^[A-Za-záéíóúÁÉÍÓÚñÑ\s]+$', nom):
            raise forms.ValidationError("El nombre solo puede contener letras y espacios.")
        return nom

    def clean_raza(self):
        raza = self.cleaned_data.get('raza')
        if len(raza) > 10:
            raise forms.ValidationError("La raza no puede tener más de 10 caracteres.")
        if not re.match(r'^[A-Za-záéíóúÁÉÍÓÚñÑ\s]+$', raza):
            raise forms.ValidationError("La raza solo puede contener letras y espacios.")
        return raza

    def clean_edad(self):
        edad = self.cleaned_data.get('edad')
        if edad and edad > datetime.date.today():
            raise forms.ValidationError("La fecha de nacimiento no puede ser en el futuro.")
        return edad

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if isinstance(photo, (InMemoryUploadedFile, TemporaryUploadedFile)):
            if photo.size > 5 * 1024 * 1024:
                raise forms.ValidationError("El archivo de imagen debe ser menor a 5MB.")
        return photo
    
class AnimalesUpdateForm(forms.ModelForm):
    
    class Meta:
        model = Animalesdb
        exclude = ['status']
        fields = ['photo', 'nom', 'edad', 'fk_esp', 'raza', 'fk_est', 'fk_tam', 'fk_gen', 'fk_user']
        widgets = {
            'edad': forms.DateInput(attrs={
                'class': 'form-control m-2 input-form',
                'type': 'date',
                'aria-label': 'Edad'
            }),
            'photo': forms.FileInput(attrs={
                'class': 'form-control m-2 input-form',
                'aria-label': 'Foto'
            }),
            'nom': forms.TextInput(attrs={
                'class': 'form-control m-2 input-form',
                'placeholder': 'Nombre del Animal',
                'aria-label': 'Nombre'
            }),
            'fk_esp': forms.Select(attrs={
                'class': 'form-control m-2 input-form custom-select',
                'aria-label': 'Especie'
            }),
            'raza': forms.TextInput(attrs={
                'class': 'form-control m-2 input-form',
                'placeholder': 'Raza del Animal',
                'aria-label': 'Raza'
            }),
            'fk_est': forms.Select(attrs={
                'class': 'form-control m-2 input-form custom-select',
                'aria-label': 'Estado'
            }),
            'fk_tam': forms.Select(attrs={
                'class': 'form-control m-2 input-form custom-select',
                'aria-label': 'Tamaño'
            }),
            'fk_gen': forms.Select(attrs={
                'class': 'form-control m-2 input-form custom-select',
                'aria-label': 'Género'
            }),
            'fk_user': forms.Select(attrs={
                'class': 'form-control m-2 input-form custom-select',
                'aria-label': 'cuidador'
            }),
        }
#formularios animales

    def __init__(self, *args, **kwargs):
        # Mostrar cedula con nombre del voluntario
        super(AnimalesUpdateForm, self).__init__(*args, **kwargs)
        self.fields['fk_user'].queryset = User.objects.all().order_by('Cedula')
        self.fields['fk_user'].label_from_instance = lambda obj: f'{obj.Cedula} - {obj.get_full_name()}'

        # Verificar si existe una instancia y si tiene un valor de 'edad'
        if self.instance and self.instance.pk and self.instance.edad:
            # Convertir la fecha a string en formato YYYY-MM-DD para el input de tipo "date"
            self.initial['edad'] = self.instance.edad.strftime('%Y-%m-%d')

    def clean_nom(self):
        nom = self.cleaned_data.get('nom')
        if len(nom) > 10:
            raise forms.ValidationError("El nombre no puede tener más de 10 caracteres.")
        if not re.match(r'^[A-Za-záéíóúÁÉÍÓÚñÑ\s]+$', nom):
            raise forms.ValidationError("El nombre solo puede contener letras y espacios.")
        return nom

    def clean_raza(self):
        raza = self.cleaned_data.get('raza')
        if len(raza) > 10:
            raise forms.ValidationError("La raza no puede tener más de 10 caracteres.")
        if not re.match(r'^[A-Za-záéíóúÁÉÍÓÚñÑ\s]+$', raza):
            raise forms.ValidationError("La raza solo puede contener letras y espacios.")
        return raza

    def clean_edad(self):
        edad = self.cleaned_data.get('edad')
        if edad and edad > datetime.date.today():
            raise forms.ValidationError("La fecha de nacimiento no puede ser en el futuro.")
        return edad

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if isinstance(photo, (InMemoryUploadedFile, TemporaryUploadedFile)):
            if photo.size > 5 * 1024 * 1024:
                raise forms.ValidationError("El archivo de imagen debe ser menor a 5MB.")
        return photo
    

#Formulario Adoptantes

class AdoptanteForm(forms.ModelForm):
    class Meta:
        model = Adoptantedb
        fields = ['photo', 'ced', 'name', 'ape', 'tlf', 'photo']
        widgets = {
            'photo': forms.FileInput(attrs={
                'class': 'form-control m-2 input-form',
                'aria-label': 'Foto'
            }),
            'ced': forms.TextInput(attrs={
                'class': 'form-control m-2 input-form',
                'placeholder': 'Cédula',
                'aria-label': 'Cédula'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control m-2 input-form',
                'placeholder': 'Nombre',
                'aria-label': 'Nombre'
            }),
            'ape': forms.TextInput(attrs={
                'class': 'form-control m-2 input-form',
                'placeholder': 'Apellido',
                'aria-label': 'Apellido'
            }),
            'tlf': forms.TextInput(attrs={
                'class': 'form-control m-2 input-form intl-tel-input',
                'placeholder': 'Teléfono',
                'aria-label': 'Teléfono'
            }),
        }
    
    def clean_ced(self):
        ced = self.cleaned_data.get('ced')

        # Validación para cédulas venezolanas: "V" o "E" seguidas de 7 u 8 dígitos
        venezuelan_pattern = r'^[V]-?\d{7,8}$'

        # Validación para cédulas colombianas: solo números, entre 6 y 10 dígitos
        colombian_pattern = r'^[C]-?\d{9,10}$'

        if not re.match(venezuelan_pattern, ced) and not re.match(colombian_pattern, ced):
            raise forms.ValidationError('La cédula debe ser válida para venezolanos (V seguido de 7-8 dígitos) o colombianos (C seguido de 9-10 dígitos).')

        return ced

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name.isalpha():
            raise forms.ValidationError('El nombre debe contener solo letras.')
        if len(name) > 10:
            raise forms.ValidationError('El nombre no puede tener más de 10 caracteres.')
        return name

    def clean_ape(self):
        ape = self.cleaned_data.get('ape')
        if not ape.isalpha():
            raise forms.ValidationError('El apellido debe contener solo letras.')
        if len(ape) > 10:
            raise forms.ValidationError('El apellido no puede tener más de 10 caracteres.')
        return ape

    def clean_tlf(self):
        tlf = self.cleaned_data.get('tlf')

        # Verificar la longitud mínima del teléfono
        if tlf and len(tlf) < 10:
            raise forms.ValidationError("El teléfono debe tener al menos 10 dígitos.")

        # Expresión regular para números venezolanos
        venezuelan_pattern = r'^(58|0)(412|416|414|426|424)\d{7}$'
        # Expresión regular para números colombianos
        colombian_pattern = r'^(57)?(3\d{2})\d{7}$'

        # Validación de números venezolanos
        if re.match(venezuelan_pattern, tlf):
            # Si empieza con "0", lo reemplazamos con "+58"
            if tlf.startswith('0'):
                tlf = '58' + tlf[1:]
            return tlf

        # Validación de números colombianos
        if re.match(colombian_pattern, tlf):
            if not tlf.startswith('57'):
                # Si no empieza con "+57", lo añadimos
                tlf = '57' + tlf
            return tlf

        # Si el número no es válido, lanzamos un error
        raise forms.ValidationError('El número de teléfono debe ser un número válido de Venezuela o Colombia.')

class AdoptanteUpdateForm(forms.ModelForm):
    class Meta:
        model = Adoptantedb
        fields = ['photo', 'name', 'ape', 'tlf', 'photo']
        widgets = {
            'photo': forms.FileInput(attrs={
                'class': 'form-control m-2 input-form',
                'aria-label': 'Foto'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control m-2 input-form',
                'placeholder': 'Nombre',
                'aria-label': 'Nombre'
            }),
            'ape': forms.TextInput(attrs={
                'class': 'form-control m-2 input-form',
                'placeholder': 'Apellido',
                'aria-label': 'Apellido'
            }),
            'tlf': forms.TextInput(attrs={
                'class': 'form-control m-2 input-form intl-tel-input',
                'placeholder': 'Teléfono',
                'aria-label': 'Teléfono'
            }),
        }
    
    def clean_ced(self):
        ced = self.cleaned_data.get('ced')

        # Validación para cédulas venezolanas: "V" o "E" seguidas de 7 u 8 dígitos
        venezuelan_pattern = r'^[V]-?\d{7,8}$'

        # Validación para cédulas colombianas: solo números, entre 6 y 10 dígitos
        colombian_pattern = r'^[C]-?\d{9,10}$'

        if not re.match(venezuelan_pattern, ced) and not re.match(colombian_pattern, ced):
            raise forms.ValidationError('La cédula debe ser válida para venezolanos (V seguido de 7-8 dígitos) o colombianos (C seguido de 9-10 dígitos).')

        return ced

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name.isalpha():
            raise forms.ValidationError('El nombre debe contener solo letras.')
        if len(name) > 10:
            raise forms.ValidationError('El nombre no puede tener más de 10 caracteres.')
        return name

    def clean_ape(self):
        ape = self.cleaned_data.get('ape')
        if not ape.isalpha():
            raise forms.ValidationError('El apellido debe contener solo letras.')
        if len(ape) > 10:
            raise forms.ValidationError('El apellido no puede tener más de 10 caracteres.')
        return ape

    def clean_tlf(self):
        tlf = self.cleaned_data.get('tlf')

        # Verificar la longitud mínima del teléfono
        if tlf and len(tlf) < 10:
            raise forms.ValidationError("El teléfono debe tener al menos 10 dígitos.")
        
        # Expresión regular para números venezolanos
        venezuelan_pattern = r'^(58|0)(412|416|414|426|424)\d{7}$'
        # Expresión regular para números colombianos
        colombian_pattern = r'^(57)?(3\d{2})\d{7}$'

        # Validación de números venezolanos
        if re.match(venezuelan_pattern, tlf):
            # Si empieza con "0", lo reemplazamos con "+58"
            if tlf.startswith('0'):
                tlf = '58' + tlf[1:]
            return tlf

        # Validación de números colombianos
        if re.match(colombian_pattern, tlf):
            if not tlf.startswith('57'):
                # Si no empieza con "+57", lo añadimos
                tlf = '57' + tlf
            return tlf

        # Si el número no es válido, lanzamos un error
        raise forms.ValidationError('El número de teléfono debe ser un número válido de Venezuela o Colombia.')

#Formulario Adopciones

class AdopcionesForm(forms.ModelForm):
    class Meta:
        model = Adopcionesdb
        fields = ['Adoptante', 'Animal', 'Fecha']
        widgets = {
            'Adoptante': forms.Select(attrs={
                'class': 'form-control m-2 input-form custom-select',
                'aria-label': 'Adoptante'
            }),
            'Animal': forms.Select(attrs={
                'class': 'form-control m-2 input-form custom-select',
                'aria-label': 'Animal'
            }),
            'Fecha': forms.DateInput(attrs={
                'class': 'form-control m-2 input-form',
                'type': 'date',
                'aria-label': 'Fecha'
            }),
        }

    
    def __init__(self, *args, **kwargs):
        super(AdopcionesForm, self).__init__(*args, **kwargs)
        
        # Cambia el queryset para 'Adoptante' para que solo muestre los adoptantes ordenados por cédula
        self.fields['Adoptante'].queryset = Adoptantedb.objects.all().order_by('ced')
        self.fields['Adoptante'].label_from_instance = lambda obj: f'{obj.ced} - {obj.name} {obj.ape}'
        
        # Cambia el queryset para 'Animal' para que solo muestre el ID del animal
        self.fields['Animal'].queryset = Animalesdb.objects.filter(status=False)
        self.fields['Animal'].label_from_instance = lambda obj: f'{obj.id} - {obj.nom}'

    # Validación personalizada para el campo 'Animal'
    def clean_Animal(self):
        animal = self.cleaned_data.get('Animal')
        # Aquí puedes agregar cualquier validación personalizada
        if animal is None:
            raise ValidationError('Debes seleccionar un animal.')
        return animal

    # Validación personalizada para el campo 'Fecha'
    def clean_Fecha(self):
        fecha = self.cleaned_data.get('Fecha')
        animal = self.cleaned_data.get('Animal')
        if fecha is None:
            raise ValidationError('Debes seleccionar una fecha.')
        if fecha > datetime.date.today():
            raise ValidationError('La fecha no puede ser futura.')
        if animal and fecha < animal.edad:
            raise ValidationError(f'El animal no puede ser adoptado antes de su fecha de nacimiento ({animal.edad}).')
        return fecha

    # Validación general del formulario
    def clean(self):
        cleaned_data = super().clean()
        adoptante = cleaned_data.get('Adoptante')
        animal = cleaned_data.get('Animal')

        if adoptante is None:
            raise ValidationError('Debes seleccionar un adoptante.')

        # Validar que un animal no sea adoptado más de una vez, excepto por el mismo adoptante
        if animal and adoptante:
            # Verificar si hay otra adopción para el mismo animal
            # Excluir la adopción actual si está en el formulario
            current_adopcion_id = self.instance.id if self.instance else None
            if Adopcionesdb.objects.filter(Animal=animal).exclude(id=current_adopcion_id).exists():
                raise ValidationError('Este animal ya ha sido adoptado por otro adoptante.')

        return cleaned_data
    
    
    
class UserForm(forms.ModelForm):
    
    class Meta:
        model = Animalesdb
        exclude = ['status']
        fields = ['photo', 'id', 'nom', 'edad', 'fk_esp', 'raza', 'fk_est', 'fk_tam', 'fk_gen',]
        widgets = {
            'edad': forms.DateInput(attrs={
                'class': 'form-control m-2 input-form',
                'type': 'date',
                'aria-label': 'Edad'
            }),
            'photo': forms.FileInput(attrs={
                'class': 'form-control m-2 input-form',
                'aria-label': 'Foto'
            }),
            'id': forms.TextInput(attrs={
                'class': 'form-control m-2 input-form',
                'placeholder': 'ID del Animal',
                'aria-label': 'ID'
            }),
            'nom': forms.TextInput(attrs={
                'class': 'form-control m-2 input-form',
                'placeholder': 'Nombre del Animal',
                'aria-label': 'Nombre'
            }),
            'fk_esp': forms.Select(attrs={
                'class': 'form-control m-2 input-form custom-select',
                'aria-label': 'Especie'
            }),
            'raza': forms.TextInput(attrs={
                'class': 'form-control m-2 input-form',
                'placeholder': 'Raza del Animal',
                'aria-label': 'Raza'
            }),
            'fk_est': forms.Select(attrs={
                'class': 'form-control m-2 input-form custom-select',
                'aria-label': 'Estado'
            }),
            'fk_tam': forms.Select(attrs={
                'class': 'form-control m-2 input-form custom-select',
                'aria-label': 'Tamaño'
            }),
            'fk_gen': forms.Select(attrs={
                'class': 'form-control m-2 input-form custom-select',
                'aria-label': 'Género'
            }),
        }
        
#formularios animales
    
    def clean_nom(self):
        nom = self.cleaned_data.get('nom')
        if len(nom) > 10:
            raise forms.ValidationError("El nombre no puede tener más de 10 caracteres.")
        if not re.match(r'^[A-Za-záéíóúÁÉÍÓÚñÑ\s]+$', nom):
            raise forms.ValidationError("El nombre solo puede contener letras y espacios.")
        return nom

    def clean_raza(self):
        raza = self.cleaned_data.get('raza')
        if len(raza) > 10:
            raise forms.ValidationError("La raza no puede tener más de 10 caracteres.")
        if not re.match(r'^[A-Za-záéíóúÁÉÍÓÚñÑ\s]+$', raza):
            raise forms.ValidationError("La raza solo puede contener letras y espacios.")
        return raza

    def clean_edad(self):
        edad = self.cleaned_data.get('edad')
        if edad and edad > datetime.date.today():
            raise forms.ValidationError("La fecha de nacimiento no puede ser en el futuro.")
        return edad

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if isinstance(photo, (InMemoryUploadedFile, TemporaryUploadedFile)):
            if photo.size > 5 * 1024 * 1024:
                raise forms.ValidationError("El archivo de imagen debe ser menor a 5MB.")
        return photo

   
class UserUpdateForm(forms.ModelForm):
    
    class Meta:
        model = Animalesdb
        exclude = ['status']
        fields = ['photo', 'nom', 'edad', 'fk_esp', 'raza', 'fk_est', 'fk_tam', 'fk_gen',]
        widgets = {
            'edad': forms.DateInput(attrs={
                'class': 'form-control m-2 input-form',
                'type': 'date',
                'aria-label': 'Edad'
            }),
            'photo': forms.FileInput(attrs={
                'class': 'form-control m-2 input-form',
                'aria-label': 'Foto'
            }),
            'nom': forms.TextInput(attrs={
                'class': 'form-control m-2 input-form',
                'placeholder': 'Nombre del Animal',
                'aria-label': 'Nombre'
            }),
            'fk_esp': forms.Select(attrs={
                'class': 'form-control m-2 input-form custom-select',
                'aria-label': 'Especie'
            }),
            'raza': forms.TextInput(attrs={
                'class': 'form-control m-2 input-form',
                'placeholder': 'Raza del Animal',
                'aria-label': 'Raza'
            }),
            'fk_est': forms.Select(attrs={
                'class': 'form-control m-2 input-form custom-select',
                'aria-label': 'Estado'
            }),
            'fk_tam': forms.Select(attrs={
                'class': 'form-control m-2 input-form custom-select',
                'aria-label': 'Tamaño'
            }),
            'fk_gen': forms.Select(attrs={
                'class': 'form-control m-2 input-form custom-select',
                'aria-label': 'Género'
            }),
        }
        
#formularios animales

    def clean_nom(self):
        nom = self.cleaned_data.get('nom')
        if len(nom) > 10:
            raise forms.ValidationError("El nombre no puede tener más de 10 caracteres.")
        if not re.match(r'^[A-Za-záéíóúÁÉÍÓÚñÑ\s]+$', nom):
            raise forms.ValidationError("El nombre solo puede contener letras y espacios.")
        return nom

    def clean_raza(self):
        raza = self.cleaned_data.get('raza')
        if len(raza) > 10:
            raise forms.ValidationError("La raza no puede tener más de 10 caracteres.")
        if not re.match(r'^[A-Za-záéíóúÁÉÍÓÚñÑ\s]+$', raza):
            raise forms.ValidationError("La raza solo puede contener letras y espacios.")
        return raza

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        # Verificar si existe una instancia y si tiene un valor de 'edad'
        if self.instance and self.instance.pk and self.instance.edad:
            # Convertir la fecha a string en formato YYYY-MM-DD para el input de tipo "date"
            self.initial['edad'] = self.instance.edad.strftime('%Y-%m-%d')

    def clean_edad(self):
        edad = self.cleaned_data.get('edad')
        if edad and edad > datetime.date.today():
            raise forms.ValidationError("La fecha de nacimiento no puede ser en el futuro.")
        return edad

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if isinstance(photo, (InMemoryUploadedFile, TemporaryUploadedFile)):
            if photo.size > 5 * 1024 * 1024:
                raise forms.ValidationError("El archivo de imagen debe ser menor a 5MB.")
        return photo


class UserEditForm(UserCreationForm):
    username = forms.CharField(
        label='Nombre de Usuario',
        max_length=10,  # Establece el límite de caracteres aquí
        widget=forms.TextInput(attrs={
            'class': 'form-control m-2 input-form',
            'placeholder': 'Ingresar Nombre de Usuario',
            'aria-label': 'Nombre de Usuario',
            'required': True
        })
    )
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control m-2 input-form',
            'placeholder': 'Ingresa tu email',
            'aria-label': 'Email',
            'required': True
        })
    )
    Cedula = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control m-2 input-form',
            'placeholder': 'Ingresa tu cédula',
            'aria-label': 'Cédula'
        })
    )
    Telefono = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control m-2 input-form',
            'placeholder': 'Ingresa tu teléfono',
            'aria-label': 'Teléfono'
        })
    )
    photo = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control m-2 input-form',
            'aria-label': 'Foto'
        })
    )
    first_name = forms.CharField(
        max_length=10,
        required=True,
        label="Nombre",
        widget=forms.TextInput(attrs={
            'class': 'form-control m-2 input-form',
            'placeholder': 'Ingresa tu nombre',
            'aria-label': 'Nombre',
            'required': True
        })
    )
    last_name = forms.CharField(
        max_length=10,
        required=True,
        label="Apellido",
        widget=forms.TextInput(attrs={
            'class': 'form-control m-2 input-form',
            'placeholder': 'Ingresa tu apellido',
            'aria-label': 'Apellido',
            'required': True
        })
    )

    password1 = forms.CharField(
        label='Contraseña',
        required=False,  # No es requerido
        widget=forms.PasswordInput(attrs={
            'class': 'form-control m-2 input-form',
            'placeholder': 'Ingresa tu contraseña',
            'aria-label': 'Contraseña',
        })
    )
    
    password2 = forms.CharField(
        label='Confirmar Contraseña',
        required=False,  # No es requerido
        widget=forms.PasswordInput(attrs={
            'class': 'form-control m-2 input-form',
            'placeholder': 'Confirma tu contraseña',
            'aria-label': 'Confirmar Contraseña',
        })
    )

    class Meta:
        model = User  # Asegúrate de que sea el modelo correcto
        fields = ['username', 'email', 'Cedula', 'Telefono', 'photo', 'first_name', 'last_name', 'password1', 'password2']
    
    # Validar que el username sea único
    def clean_username(self):
        username = self.cleaned_data.get('username')

        # Validar que el username contenga solo letras y tenga un máximo de 10 caracteres
        if not re.match(r'^[a-zA-Z]{1,10}$', username):
            raise forms.ValidationError('El nombre de usuario solo puede contener letras y debe tener un máximo de 10 caracteres.')

        # Obtener el usuario actual del formulario
        user_instance = self.instance

        # Comprobar si ya existe un usuario con ese nombre de usuario, pero permitir que sea el mismo que el del usuario actual
        if User.objects.filter(username=username).exclude(pk=user_instance.pk).exists():
            raise forms.ValidationError('El nombre de usuario ya está en uso.')

        return username
    # Validación de cédula única y formato
    def clean_Cedula(self):
        Cedula = self.cleaned_data.get('Cedula')
        current_user = self.instance

        # Expresiones regulares para validación
        venezolana_regex = r'^V-?\d{7,8}$'
        colombiana_regex = r'^C-?\d{9,10}$'

        # Verificar si la cédula ya está en uso
        if User.objects.filter(Cedula=Cedula).exclude(id=current_user.id).exists():
            raise forms.ValidationError("Esta cédula ya está en uso.")

        # Validación del formato de cédula
        if not (re.match(venezolana_regex, Cedula) or re.match(colombiana_regex, Cedula)):
            raise forms.ValidationError('La cédula debe ser válida para venezolanos (V seguido de 7-8 dígitos) o colombianos (C seguido de 9-10 dígitos).')
        return Cedula
    
    # Validación del teléfono
    def clean_Telefono(self):
        Telefono = self.cleaned_data.get('Telefono')

        # Verificar si el teléfono contiene solo números
        if Telefono and not re.match(r'^\+?\d+$', Telefono):
            raise forms.ValidationError("El teléfono solo debe contener números.")

        # Verificar la longitud mínima del teléfono
        if Telefono and len(Telefono) < 10:
            raise forms.ValidationError("El teléfono debe tener al menos 10 dígitos.")

        # Validar formatos de teléfono
        colombian_pattern = r'^(57)?(3\d{2})\d{7}$'
        venezuelan_pattern = r'^(58|0)?(412|416|414|426|424)\d{7}$'

        # Validación de números venezolanos
        if re.match(venezuelan_pattern, Telefono):
            # Si empieza con "0", lo reemplazamos con "+58"
            if Telefono.startswith('0'):
                Telefono = '58' + Telefono[1:]
            return Telefono

        # Validación de números colombianos
        if re.match(colombian_pattern, Telefono):
            if not Telefono.startswith('57'):
                # Si no empieza con "+57", lo añadimos
                Telefono = '57' + Telefono
            return Telefono

        # Si el número no es válido, lanzamos un error
        raise forms.ValidationError("El número de teléfono debe ser un número válido de Venezuela o Colombia.")
    
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not re.match("^[A-Za-záéíóúÁÉÍÓÚñÑ]+$", first_name):
            raise forms.ValidationError("El nombre solo debe contener letras.")
        return first_name
    
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not re.match("^[A-Za-záéíóúÁÉÍÓÚñÑ]+$", last_name):
            raise forms.ValidationError("El apellido solo debe contener letras.")
        return last_name

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 or password2:  # Solo validamos si se ingresó algo en password1 o password2
            if password1 != password2:
                raise forms.ValidationError("Las contraseñas no coinciden.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        
        # Solo establecer una nueva contraseña si se proporcionó
        password1 = self.cleaned_data.get('password1')
        if password1:  # Solo se cambia la contraseña si se ingresó una nueva
            user.set_password(password1)

        if commit:
            user.save()
        return user
