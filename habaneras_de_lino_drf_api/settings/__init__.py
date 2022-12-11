import environ
from .base import *

DEBUG = True

env = environ.Env()
environ.Env.read_env()

# Get current environment to load configs
try:
    CURRENT_ENV = env("CURRENT_ENV")

except CURRENT_ENV is None:
    CURRENT_ENV = 'DEVELOPMENT'


# Load configs
if CURRENT_ENV == "DEVELOPMENT":
    from .dev import *
elif CURRENT_ENV == "PRODUCTION":
    from .prod import *
else:
    from .docker import *
