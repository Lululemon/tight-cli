import sys
import os

import logging
from logging.config import dictConfig

logging_config = dict(
    version=1,
    formatters={
        'f': {'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'}
    },
    handlers={
        'h': {'class': 'logging.StreamHandler',
              'formatter': 'f',
              'level': logging.INFO}
    },
    root={
        'handlers': ['h'],
        'level': logging.INFO,
    },
)

dictConfig(logging_config)

here = os.path.dirname(os.path.realpath(__file__))
sys.path = [os.path.join(here, "./vendored")] + sys.path
sys.path = [os.path.join(here, "./lib")] + sys.path
sys.path = [os.path.join(here, "./models")] + sys.path
sys.path = [os.path.join(here, "./serializers")] + sys.path
sys.path = [os.path.join(here, "../")] + sys.path
