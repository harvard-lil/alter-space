import os
import requests
import urllib.parse
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
            if is_sound_filepath(f):
                name = urllib.parse.unquote(f)
                music_files.append(name)
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
                name = urllib.parse.unquote(href)
                sound_urls.append(name)
        return sound_urls
