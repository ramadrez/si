from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

##Prueba de usuarios 

class User(AbstractUser):

    photo = models.ImageField(default="User_default.jpg",upload_to="Users/")
    Cedula = models.CharField(max_length=50, null=True,blank=True)
    Telefono= models .CharField(max_length=50, null=True,blank=True)

    def __str__(self) -> str:
        return self.username
    
##TABLA DE GENEROS    
class Generodb(models.Model):
    gen= models.CharField(max_length=20, verbose_name= "Genero")

    class Meta:
        db_table="Generos"
        verbose_name ="Generos"

    def __str__(self) -> str:
        return self.gen

##TABLA DE ESTELIRIZACION
class Esterilizaciondb(models.Model):
    est= models.CharField(max_length=20, verbose_name= "Genero")

    class Meta:
        db_table="Esterilizacion"
        verbose_name ="Estelirizacion"

    def __str__(self) -> str:
        return self.est
    

## TABLA DE SIZES    
class Tamañodb(models.Model):
    tamaño= models.CharField(max_length=20, verbose_name= "Genero")

    class Meta:
        db_table="Tamaño"
        verbose_name ="Tamaño"

    def __str__(self) -> str:
        return self.tamaño

## TABLA DE ESPECIES GATO/PERRO, pero como puede escalar vamos a dar la opcion de que ingresen la especie de animal    
class Tipodb(models.Model):
    especie= models.CharField(max_length=20, verbose_name= "Especie")

    class Meta:
        db_table="Tipo"
        verbose_name ="Tipos"
        verbose_name_plural= "Tipos"

    def __str__(self) -> str:
        return self.especie
    

## ESTOS SON LOS ADOPTANTES
class Adoptantedb(models.Model):
    ced= models.CharField(max_length=60,primary_key=True,verbose_name="Cedula" )
    name= models.CharField(max_length=30, verbose_name= "Nombre")
    ape= models.CharField(max_length=30, verbose_name= "Apellido")
    tlf= models.CharField(max_length=100,verbose_name= "Telefono")
    photo = models.ImageField(default="Adoptante_default.png",upload_to="Adoptante/")
    
    class Meta:
        db_table="Adoptantes"
        verbose_name ="Adoptante"
        verbose_name_plural= "Adoptantes"

    def __str__(self) -> str:
        return self.ced

    
##ESTOS SON LOS ANIMALES/ HAY UN bug QUE EVITA QUE RETORNE UN STR, POR ESO EN SUPER ADMIN EL NOMBRE LO RETORNA COMO Animalesdb object
##Se buguea en la tabla de resguardos
class Animalesdb(models.Model):
    id= models.AutoField(primary_key=True,verbose_name="ID",default=None)
    nom= models.CharField(max_length=50, verbose_name= "Nombre")
    edad= models.DateField(verbose_name= "Fecha de nacimiento aprox.")
    status= models.BooleanField(verbose_name= "Status_adopcion",default=False)
    raza= models.CharField(max_length=30, verbose_name= "Raza")
    fk_est=  models.ForeignKey(Esterilizaciondb, on_delete=models.CASCADE,verbose_name= "Estelirizacion")
    fk_esp= models.ForeignKey(Tipodb, on_delete=models.CASCADE, verbose_name="Especie",default=None)
    fk_tam=  models.ForeignKey(Tamañodb, on_delete=models.CASCADE, verbose_name= "Tamaño")
    fk_gen=  models.ForeignKey(Generodb, on_delete= models.CASCADE, verbose_name= "Genero")
    fk_user= models.ForeignKey(User,on_delete= models.CASCADE, verbose_name= "CI_cuidador",default=None)
    photo = models.ImageField(default="Animal_default.jpg",upload_to="Animal/")

    class Meta:
        db_table="Animales"
        verbose_name ="Animal"
        verbose_name_plural= "Animales"

    def __str__(self) -> str:
    
        return self.nom

        
##TABLA DE ADOPCIONES
class Adopcionesdb(models.Model):
    id= models.AutoField(primary_key=True,verbose_name="Id",default=None) 
    Adoptante= models.ForeignKey(Adoptantedb,on_delete=models.CASCADE)
    Animal= models.ForeignKey(Animalesdb,on_delete=models.CASCADE)
    Fecha= models.DateField(verbose_name="Fecha de adopcion")

    class Meta:
        db_table="Adopciones"
        verbose_name ="Adopciones"
        verbose_name_plural= "Adopciones"
        

    def __str__(self) -> str:
            return self.id
    
