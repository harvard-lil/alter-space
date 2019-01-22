import os

DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')

ACTIVITIES = ["relax",
              "study",
              "meditate",
              "focus",
              "create",
              "be weird"]

# LIGHTS
LIGHTS_TOKEN = "abc"
LIGHTS_ID = "xyz"
LIGHT_PRESETS = {
    "relax": ["some_id", "some_other_id"],
    "study": ["123"],
    "meditate": ["234", "456", "789"],
    "focus": ["9", "1"],
    "create": ["0"],
    "be weird": ["4", "8"]
}


SOUND_PRESETS = {
    "relax": [0, 3],
    "study": [1, 9, 5],
    "meditate": [8],
    "focus": [6, 3],
    "create": [2, 3, 4],
    "be weird": [4, 8]
}
