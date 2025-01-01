from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import getpass
import uuid

class Command(BaseCommand):
     help = 'Create a superuser using a username'

     def handle(self, *args, **options):
         User = get_user_model()
         username = input('Username: ')
         email = input('Email address: ')
         password = getpass.getpass('Password: ')
         password_confirm = getpass.getpass('Password (again): ')

         if password != password_confirm:
             self.stderr.write('Passwords do not match, please try again.')
             return

         try:
            username_check = username
            if User.objects.filter(username=username).exists():
                username_check = f'{username}-{uuid.uuid4().hex[:5]}'
            User.objects.create_superuser(username=username_check, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f'Superuser with username {username} created successfully.'))
         except Exception as e:
             self.stderr.write(f'Error creating superuser: {e}')