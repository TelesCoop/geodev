from django.contrib.staticfiles.storage import ManifestStaticFilesStorage

from .base import *  # noqa: F401,F403

import getconf

DEBUG = False
config = getconf.ConfigGetter(
    "geodev",
    ["/etc/telescoop/geodev/settings.ini", "./local_settings.ini"],
)
SECRET_KEY = config.getstr("security.secret_key")
ALLOWED_HOSTS = config.getlist("security.allowed_hosts", [])
STATIC_ROOT = config.getstr("staticfiles.static_root")

try:
    from .local import *  # noqa: F401,F403
except ImportError:
    pass

MIDDLEWARE.append(  # noqa: F405
    "rollbar.contrib.django.middleware.RollbarNotifierMiddleware"
)

ROLLBAR = {
    "access_token": config.getstr("bugs.rollbar_access_token"),
    "environment": "development" if DEBUG else "production",
    "root": BASE_DIR,  # noqa: F405
}
import rollbar  # noqa: E402

rollbar.init(**ROLLBAR)


# some {% static 'xxx' %} path dont exist, and we don't want to raise an error
class MyFileStorage(ManifestStaticFilesStorage):
    manifest_strict = False


STATICFILES_STORAGE = "geodev.settings.production.MyFileStorage"

BACKUP_ACCESS = config.getstr("backup.backup_access")  # S3 ACCESS
BACKUP_SECRET = config.getstr("backup.backup_access")  # S3 SECRET KEY
BACKUP_BUCKET = "geodev-backup"  # S3 Bucket
BACKUP_KEEP_N_DAYS = 31  # Optional, defaults to 31
BACKUP_REGION = "eu-west-3"  # Optional, defaults to eu-west-3 (Paris)
BACKUP_HOST = "s3.eu-west-3.amazonaws.com"  # Optional, default to s3.{BACKUP_REGIOn}.amazonaws.com
