import os
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Cria um superusuário admin a partir de variáveis de ambiente.'

    def handle(self, *args, **options):
        User = get_user_model()
        username = os.getenv('DJANGO_SUPERUSER_USERNAME', 'root')
        email = os.getenv('DJANGO_SUPERUSER_EMAIL', 'root@example.com')
        password = os.getenv('DJANGO_SUPERUSER_PASSWORD')

        if not password:
            self.stderr.write(self.style.ERROR(
                'Defina DJANGO_SUPERUSER_PASSWORD antes de rodar o comando.'
            ))
            return

        user, created = User.objects.get_or_create(
            username=username,
            defaults={'email': email, 'is_staff': True, 'is_superuser': True},
        )
        user.email = email
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save()

        msg = 'criado' if created else 'atualizado'
        self.stdout.write(self.style.SUCCESS(
            f"Superusuário '{username}' {msg} com sucesso."
        ))
