# from backend.views import backend_app
from flask import url_for

def test_homepage(client):
    response = client.get(url_for('backend.index'))
    assert response.status_code == 200


def test_sounds(client):
    response = client.get(url_for('backend.sounds'))
    assert response.status_code == 200
    assert type(response.json) is dict
    results = response.json
    assert 'nature' in results
    for song in results['nature']:
        assert ".mp3" in song or ".wav" in song


def test_activity(client):
    response = client.get(url_for('backend.get_activity_presets', activity='focus'))
    assert response.status_code == 200
    assert type(response.json) is dict
    result = response.json
    assert "light" in result.keys()
    assert "sound" in result.keys()
