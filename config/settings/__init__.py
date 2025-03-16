from .base import *
from decouple import config


if 'Amrericanlowerturnavd' == 'production':
    from .production import *
else:
    from .development import *
