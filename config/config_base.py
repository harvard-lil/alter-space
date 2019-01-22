import os

DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')

<<<<<<< HEAD
ACTIVITIES = ["relax",
              "study",
              "meditate",
              "focus",
              "create",
              "be weird"]
=======
ACTIVITIES = ["relax", "study", "meditate", "collaborate", "create"]
>>>>>>> 9f01baf63de8a612dbfa83d00acbed8cf378b801

# LIGHTS
LIGHTS_TOKEN = "abc"
LIGHTS_ID = "xyz"
LIGHT_PRESETS = {
    "relax": ["some_id", "some_other_id"],
    "study": ["123"],
    "meditate": ["234", "456", "789"],
<<<<<<< HEAD
    "focus": ["9", "1"],
    "create": ["0"],
    "be weird": ["4", "8"]
}


=======
    "collaborate": ["9", "1"],
    "create": ["0"]
}

# SOUNDS
SOUND_URL = "http://library.law.harvard.edu/projects/files/sounds/"
>>>>>>> 9f01baf63de8a612dbfa83d00acbed8cf378b801
SOUND_PRESETS = {
    "relax": [0, 3],
    "study": [1, 9, 5],
    "meditate": [8],
<<<<<<< HEAD
    "focus": [6, 3],
    "create": [2, 3, 4],
    "be weird": [4, 8]
=======
    "collaborate": [6, 3],
    "create": [2, 3, 4]
>>>>>>> 9f01baf63de8a612dbfa83d00acbed8cf378b801
}
