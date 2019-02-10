import os

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
SOUND_URL = "http://library.law.harvard.edu/projects/files/sounds/"

CELERY_BROKER_URL = 'redis://',
CELERY_RESULT_BACKEND = 'redis://'
CELERY_TASK_ALWAYS_EAGER = False
