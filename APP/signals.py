from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image
from .models import Animalesdb,Adoptantedb,User

@receiver(post_save, sender=Animalesdb)
def optimize_image(sender, instance, **kwargs):
    if instance.photo:
        photo_path = instance.photo.path
        image = Image.open(photo_path)

        # Aquí puedes ajustar el tamaño o calidad
        max_size = (800, 800)
        image.thumbnail(max_size)

        # Optimizar y sobrescribir la imagen
        image.save(photo_path, optimize=True, quality=85)



@receiver(post_save, sender=Adoptantedb)
def optimize_image(sender, instance, **kwargs):
    if instance.photo:
        photo_path = instance.photo.path
        image = Image.open(photo_path)

        # Ajusta el tamaño máximo permitido para la imagen (por ejemplo, 800x800)
        max_size = (800, 800)
        image.thumbnail(max_size)

        # Optimiza la imagen y la guarda nuevamente
        image.save(photo_path, optimize=True, quality=85)
        
        
@receiver(post_save, sender=User)
def optimize_user_image(sender, instance, **kwargs):
    if instance.photo:  # Si el usuario tiene una foto
        photo_path = instance.photo.path
        img = Image.open(photo_path)
        if img.height > 800 or img.width > 800:
            img.thumbnail((800, 800))
            img.save(photo_path)  # Guarda la imagen optimizada