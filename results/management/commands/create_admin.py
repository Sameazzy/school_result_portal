import os

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Create or update the production superuser"

    def handle(self, *args, **kwargs):
        User = get_user_model()

        username = os.environ.get("DJANGO_ADMIN_USERNAME")
        email = os.environ.get("DJANGO_ADMIN_EMAIL")
        password = os.environ.get("DJANGO_ADMIN_PASSWORD")

        if not all([username, email, password]):
            self.stdout.write(
                self.style.ERROR(
                    "DJANGO_ADMIN_USERNAME, DJANGO_ADMIN_EMAIL and "
                    "DJANGO_ADMIN_PASSWORD must be set."
                )
            )
            return

        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "email": email,
                "is_staff": True,
                "is_superuser": True,
            },
        )

        user.email = email
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save()

        self.stdout.write(
            self.style.SUCCESS(
                f"Admin {'created' if created else 'updated'}: {username}"
            )
        )