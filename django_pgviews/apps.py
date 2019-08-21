import logging

from django import apps
from django.db.models import signals
from django.utils.module_loading import import_string

from .settings import PGVIEW_SYNC_VIEW_PATH

log = logging.getLogger('django_pgviews.sync_pgviews')


class ViewSyncLauncher(object):
    counter = 0

    @classmethod
    def sync_pgviews(cls, sender, app_config, **kwargs):
        """Forcibly sync the views.
        """
        cls.counter = cls.counter + 1
        total = len([a for a in apps.apps.get_app_configs() if a.models_module is not None])

        if cls.counter == total:
            log.info('All applications have migrated, time to sync')
            # Import here otherwise Django doesn't start properly
            # (models in app init are not allowed)
            from .models import ViewSyncer
            vs = ViewSyncer()
            vs.run(force=True, update=True)


sync_pgviews = ViewSyncLauncher.sync_pgviews


class ViewConfig(apps.AppConfig):
    """The base configuration for Django PGViews. We use this to setup our
    post_migrate signal handlers.
    """
    name = 'django_pgviews'
    verbose_name = 'Django Postgres Views'

    def ready(self):
        """Find and setup the apps to set the post_migrate hooks for.
        """
        import ipdb; print("\a"); ipdb.sset_trace()
        sync_pgviews = import_string(PGVIEW_SYNC_VIEW_PATH)
        signals.post_migrate.connect(sync_pgviews)
