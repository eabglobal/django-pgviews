from django.conf import settings as base_settings

PGVIEW_SYNC_VIEW_PATH = getattr(base_settings, 'PGVIEW_SYNC_VIEW_PATH', 'django_pgviews.apps.sync_pgviews')
