from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    # let the app know about signals(connect signals)
    def ready(self):
        '''make sure to type import not return'''
        import users.signals