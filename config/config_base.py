import os

DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')

SOUND_URL = "http://library.law.harvard.edu/projects/files/sounds/"
LIGHTS_TOKEN = "abc"
LIGHTS_ID = "xyz"

ACTIVITIES = ["relax", "study", "meditate", "collaborate", "create"]

SOUND_PRESETS = {
    "relax": [0, 3],
    "study": [1, 9, 5],
    "meditate": [8],
    "collaborate": [6, 3],
    "create": [2, 3, 4]
}

LIGHT_PRESETS = {
    "relax": ["some_id", "some_other_id"],
    "study": ["123"],
    "meditate": ["234", "456", "789"],
    "collaborate": ["9", "1"],
    "create": ["0"]
}
