import os

# logging levels: 10 = debug, 20 = info, 30 = warning, 40 = error
LOG_LEVEL = 10
LOG_FILENAME = "alterspace.log"
LOG_FORMAT = '%(levelname)s: %(message)s'

DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')

ACTIVITIES = ["relax",
              "read",
              "meditate",
              "focus",
              "create",
              "wyrd"]
# LIGHTS
LIGHTS_TOKEN = "abc"
LIGHTS_ID = "xyz"

# SOUNDS
# SOUND_URL = "http://library.law.harvard.edu/projects/files/sounds/"
SOUND_URL = "http://127.0.0.1:5000/sounds"
CELERY_BROKER_URL = 'redis://',
CELERY_RESULT_BACKEND = 'redis://'
CELERY_TASK_ALWAYS_EAGER = False

SOUND_USE_LOCAL = True