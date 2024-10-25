from django.apps import AppConfig


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'APP'
    
    def ready(self):
        import APP.signals  # Asegúrate de que 'APP.signals' sea el nombre correcto de tu aplicación
