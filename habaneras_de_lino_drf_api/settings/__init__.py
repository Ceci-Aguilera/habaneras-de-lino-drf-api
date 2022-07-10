import environ
from .base import *

DEBUG = True

env = environ.Env()
environ.Env.read_env()

try:
    CURRENT_ENV = env("CURRENT_ENV")

except CURRENT_ENV is None:
    CURRENT_ENV = 'PRODUCTION'

if CURRENT_ENV == "DEVELOPMENT":
    from .dev import *
elif CURRENT_ENV == "PRODUCTION":
    from .prod import *
else:
    from .docker import *
