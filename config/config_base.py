import os

DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')

ACTIVITIES = ["relax",
              "read",
              "meditate",
              "focus",
              "create",
              "be weird"]
# LIGHTS
LIGHTS_TOKEN = "abc"
LIGHTS_ID = "xyz"
LIGHT_PRESETS = {
    "relax": ["some_id", "some_other_id"],
    "read": ["123"],
    "meditate": ["234", "456", "789"],
    "focus": ["9", "1"],
    "create": ["0"],
    "be weird": ["4", "8"]
}

# SOUNDS
SOUND_URL = "http://library.law.harvard.edu/projects/files/sounds/"

SOUND_PRESETS = {
    "relax": [0, 3],
    "read": [1, 9, 5],
    "meditate": [8],
    "be weird": [4, 8],
    "focus": [6, 3],
    "create": [2, 3, 4],
}

# relax = {
#     "states": [
#         {
#             "selector": "d073d52cd4cb",
#             "connected": "true",
#             "power": "on",
#             "color": {
#                 "hue": 299.9972533760586,
#                 "saturation": 1,
#                 "kelvin": 3500
#             },
#             "brightness": 0.09782558937972076,
#             "zones": {
#                 "count": 16,
#                 "zones": [
#                     {
#                         "brightness": 0.1,
#                         "hue": 300,
#                         "kelvin": 3500,
#                         "saturation": 1,
#                         "zone": 0
#                     },
#                     {
#                         "brightness": 0.1,
#                         "hue": 285.5,
#                         "kelvin": 3500,
#                         "saturation": 0.94,
#                         "zone": 1
#                     },
#                     {
#                         "brightness": 0.1,
#                         "hue": 271,
#                         "kelvin": 3500,
#                         "saturation": 0.87,
#                         "zone": 2
#                     },
#                     {
#                         "brightness": 0.1,
#                         "hue": 256.5,
#                         "kelvin": 3500,
#                         "saturation": 0.81,
#                         "zone": 3
#                     },
#                     {
#                         "brightness": 0.1,
#                         "hue": 249.25,
#                         "kelvin": 3500,
#                         "saturation": 0.78,
#                         "zone": 4
#                     },
#                     {
#                         "brightness": 0.1,
#                         "hue": 242,
#                         "kelvin": 3500,
#                         "saturation": 0.75,
#                         "zone": 5
#                     },
#                     {
#                         "brightness": 0.1,
#                         "hue": 243.5,
#                         "kelvin": 3500,
#                         "saturation": 0.81,
#                         "zone": 6
#                     },
#                     {
#                         "brightness": 0.1,
#                         "hue": 245,
#                         "kelvin": 3500,
#                         "saturation": 0.87,
#                         "zone": 7
#                     },
#                     {
#                         "brightness": 0.1,
#                         "hue": 246.5,
#                         "kelvin": 3500,
#                         "saturation": 0.94,
#                         "zone": 8
#                     },
#                     {
#                         "brightness": 0.1,
#                         "hue": 247.25,
#                         "kelvin": 3500,
#                         "saturation": 0.97,
#                         "zone": 9
#                     },
#                     {
#                         "brightness": 0.1,
#                         "hue": 248,
#                         "kelvin": 3500,
#                         "saturation": 1,
#                         "zone": 10
#                     },
#                     {
#                         "brightness": 0.1,
#                         "hue": 227,
#                         "kelvin": 3500,
#                         "saturation": 1,
#                         "zone": 11
#                     },
#                     {
#                         "brightness": 0.1,
#                         "hue": 206,
#                         "kelvin": 3500,
#                         "saturation": 0.99,
#                         "zone": 12
#                     },
#                     {
#                         "brightness": 0.1,
#                         "hue": 185,
#                         "kelvin": 3500,
#                         "saturation": 0.99,
#                         "zone": 13
#                     },
#                     {
#                         "brightness": 0.1,
#                         "hue": 174.49,
#                         "kelvin": 3500,
#                         "saturation": 0.99,
#                         "zone": 14
#                     },
#                     {
#                         "brightness": 0.1,
#                         "hue": 164,
#                         "kelvin": 3500,
#                         "saturation": 0.99,
#                         "zone": 15
#                     }
#                 ]
#             },
#             "effect": "OFF",
#             "group": {
#                 "id": "2354c5f275b85bea5eddd7e85db3261c",
#                 "name": "Living Room"
#             },
#             "location": {
#                 "id": "f620c86f7f4ed80c9185e14cd3daf466",
#                 "name": "Alter Space"
#             },
#             "product": {
#                 "name": "LIFX Z",
#                 "identifier": "lifx_z2",
#                 "company": "LIFX",
#                 "capabilities": {
#                     "has_color": "true",
#                     "has_variable_color_temp": "true",
#                     "has_ir": "false",
#                     "has_chain": "false",
#                     "has_multizone": "true",
#                     "min_kelvin": 2500,
#                     "max_kelvin": 9000
#                 }
#             },
#             "last_seen": "2019-01-28T23:27:13Z",
#             "seconds_since_seen": 0
#         }
#     ]
# }
