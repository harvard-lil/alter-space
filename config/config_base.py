import os

DEBUG = True
USE_LIGHT_FIXTURES = False

# logging levels: 10 = debug, 20 = info, 30 = warning, 40 = error
LOG_LEVEL = 10
LOG_FILENAME = "alterspace.log"
LOG_FORMAT = '%(levelname)s: %(message)s'

DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')

ALTERSPACE_IP = "127.0.0.1"

ACTIVITIES = ["focus",
              "meditate",
              "read",
              "relax",
              "create",
              "wyrd"]
# LIGHTS
LIGHTS_TOKEN = "abc"
LIGHTS_ID = "xyz"

# SOUNDS
CELERY_BROKER_URL = 'redis://',
CELERY_RESULT_BACKEND = 'redis://'
CELERY_TASK_ALWAYS_EAGER = False

SOUND_USE_LOCAL = True

LIGHT_STORE_DIR = os.path.join(DIR, 'backend/lightstore')

# a string to append to any light that has multiple colors, like a light strip or beam
MULTICOLOR_INDICATOR = "_multizone_"
LIGHT_STEPS = 28
