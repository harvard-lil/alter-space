import os
import requests
from bs4 import BeautifulSoup

from config import config


def is_sound_filepath(url):
    return ".wav" in url or ".mp3" in url


def get_sound_paths(sound_type='nature'):
    """
    Returns a list of all sound file urls
    """

    if config.SOUND_USE_LOCAL:
        sound_dir = os.path.join(config.DIR, "sounds")
        all_files = os.listdir(os.path.join(sound_dir, sound_type))
        music_files = []
        for f in all_files:
            if f[-4:] == ".mp3":
                music_files.append(f)
        return music_files
    else:
        sound_dir = os.path.join(config.SOUND_URL, sound_type)
        res = requests.get(sound_dir)
        soup = BeautifulSoup(res.text, 'html.parser')
        a_tags = soup.findAll('a')
        sound_urls = []
        for a_tag in a_tags:
            href = a_tag.get('href')
            if is_sound_filepath(href):
                sound_urls.append(href)
        return sound_urls
