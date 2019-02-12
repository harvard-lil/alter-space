# from backend.views import backend_app
from flask import url_for
from backend.views import *


# def test_some_endpoint(client):
#     assert client.post(url_for('some_endpoint'),
#            data=json.dumps(dict(some_attr='some_value')),
#            content_type='application/json').status_code == 200

def test_homepage(client):
    response = client.get(url_for('backend.index'))
    assert response.status_code == 200


def test_sounds(client):
    response = client.get('/sounds')
    assert response.status_code == 200
    assert response.is_json
    results = response.get_json()
    assert 'nature' in results
    for song in results['nature']:
        assert ".mp3" in song or ".wav" in song


def test_activity(client):
    response = client.get('/activity/relax')
    assert response.status_code == 200
    assert response.is_json
    result = response.get_json()
    assert "light" in result.keys()
    assert "sound" in result.keys()

    sound = result['sound']
