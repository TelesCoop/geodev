from .base import *  # noqa: F401,F403

DEBUG = False

try:
    from .local import *  # noqa: F401,F403
except ImportError:
    pass

MIDDLEWARE.append(  # noqa: F405
    "rollbar.contrib.django.middleware.RollbarNotifierMiddleware"
)

ROLLBAR = {
    "access_token": "43c4b59af5d14116a7077bc2612df1e0",
    "environment": "development" if DEBUG else "production",
    "root": BASE_DIR,  # noqa: F405
}
import rollbar  # noqa: E402

rollbar.init(**ROLLBAR)
