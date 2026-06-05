#!/usr/bin/env python
import os
import sys
import inspect
from collections import defaultdict

# Ensure project root is importable when running this script directly.
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "digipal.settings")
import django
django.setup()

from django.conf import settings
try:
    from django.urls import get_resolver, get_urlconf
except ImportError:
    from django.core.urlresolvers import get_resolver, get_urlconf
from django.apps import apps
from django.db import models
from django.core.management import find_commands, load_command_class
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType

def print_header(title):
    print("\n" + "=" * 80)
    print("  {}".format(title))
    print("=" * 80 + "\n")

def list_urls():
    print_header("URL PATTERNS (Endpoints)")
    resolver = get_resolver(get_urlconf())

    def print_urls(urlpatterns, prefix=""):
        for pattern in urlpatterns:
            path = prefix + str(pattern.pattern)
            if hasattr(pattern, 'url_patterns'):  # Nested URLs (e.g., include())
                print_urls(pattern.url_patterns, path)
            else:
                view = pattern.callback if pattern.callback else pattern._callback_str
                methods = getattr(pattern, 'methods', ['ALL'])
                print("  {} | {} | Methods: {}".format(path.ljust(40), str(view).ljust(50), methods))

    print_urls(resolver.url_patterns)

def list_models():
    print_header("MODELS (Database Tables)")
    for model in apps.get_models():
        fields = []
        for field in model._meta.get_fields():
            if hasattr(field, 'name'):
                field_type = field.__class__.__name__
                fields.append("{} ({})".format(field.name, field_type))
        print("  {} ({})".format(model.__name__, model._meta.app_label))
        print("    Fields: {}".format(', '.join(fields)))
        print("    App: {}".format(model._meta.app_label))
        print()

def list_forms():
    print_header("FORMS (Validation Rules)")
    for app_config in apps.get_app_configs():
        forms_module = None
        try:
            forms_module = __import__("{}.forms".format(app_config.name), fromlist=[""])
        except ImportError:
            continue

        for name, obj in inspect.getmembers(forms_module):
            if inspect.isclass(obj) and issubclass(obj, __import__("django.forms", fromlist=[""]).forms.ModelForm):
                print("  {} (ModelForm)".format(name))
                print("    Model: {}".format(obj._meta.model.__name__))
                print("    Fields: {}".format(list(obj.base_fields.keys())))
                print()

def list_middleware():
    print_header("MIDDLEWARE (Request/Response Processing)")
    middleware_list = getattr(settings, 'MIDDLEWARE', None) or getattr(settings, 'MIDDLEWARE_CLASSES', [])
    for middleware in middleware_list:
        print("  {}".format(middleware))

def list_management_commands():
    print_header("CUSTOM MANAGEMENT COMMANDS")
    for app_config in apps.get_app_configs():
        commands = find_commands(app_config.path)
        for cmd in commands:
            cmd_class = load_command_class(app_config.name, cmd)
            print("  {} | {}".format(cmd.ljust(20), cmd_class.help))

def list_signals():
    print_header("SIGNALS (Event Handlers)")
    from django.db.models.signals import pre_save, post_save, pre_delete, post_delete
    from django.dispatch import Signal

    signals = [
        ("pre_save", pre_save),
        ("post_save", post_save),
        ("pre_delete", pre_delete),
        ("post_delete", post_delete),
    ]

    for name, signal in signals:
        receivers = signal.receivers
        if receivers:
            print("  {}:".format(name.upper()))
            for receiver, _ in receivers:
                print("    - {} (from {})".format(getattr(receiver, '__name__', str(receiver)), getattr(receiver, '__module__', 'unknown')))

def list_third_party_apps():
    print_header("THIRD-PARTY APPS (Integrations)")
    for app_config in apps.get_app_configs():
        if not app_config.name.startswith("django."):
            print("  {} (Version: {})".format(app_config.name, getattr(app_config, 'version', 'Unknown')))

def list_user_roles():
    print_header("USER ROLES & PERMISSIONS")
    print("  Built-in Django roles:")
    for group in Group.objects.all():
        print("    - {} (Permissions: {})".format(group.name, group.permissions.count()))

    print("\n  Permissions by app:")
    for app in apps.get_app_configs():
        if app.name.startswith("django."):
            continue
        perms = Permission.objects.filter(content_type__app_label=app.label)
        if perms:
            print("    - {}: {} permissions".format(app.label, perms.count()))

def list_templates():
    print_header("TEMPLATES (Frontend Views)")
    template_dirs = settings.TEMPLATES[0]['DIRS'] if settings.TEMPLATES else []
    print("  Template directories: {}".format(template_dirs))

    # Note: Full template listing requires manual inspection (Django doesn't expose this easily)
    print("  Note: Use `find . -name '*.html'` to list template files manually.")

def list_apis():
    print_header("APIS (REST/GraphQL Endpoints)")
    # This is a simplified check; use OpenAPI/Swagger for full API docs
    print("  Check `urls.py` for API endpoints (e.g., `/api/`, `/graphql/`).")
    print("  Common Django REST Framework patterns:")
    print("    - `/api/posts/` -> PostListView")
    print("    - `/api/posts/<id>/` -> PostDetailView")

def main():
    print_header("DJANGO APP FEATURE LISTING")
    print("Project: {}".format(settings.INSTALLED_APPS[0].split('.')[0]))
    print("Django Version: {}".format(django.get_version()))

    list_urls()
    list_models()
    list_forms()
    list_middleware()
    list_management_commands()
    list_signals()
    list_third_party_apps()
    list_user_roles()
    list_templates()
    list_apis()

if __name__ == "__main__":
    main()
