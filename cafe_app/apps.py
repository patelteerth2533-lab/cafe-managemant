from django.apps import AppConfig
from django.db.models.signals import post_migrate


def auto_seed_on_migrate(sender, **kwargs):
    if sender.name == "cafe_app":
        try:
            from .seed_helper import ensure_seed_data
            ensure_seed_data(quiet=True)
        except Exception:
            pass


class CafeAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "cafe_app"

    def ready(self):
        post_migrate.connect(auto_seed_on_migrate, sender=self)
