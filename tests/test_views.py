def test_homepage(client):
    response = client.get('/')
    assert response.status_code == 200


def test_sounds(client):
    response = client.get('/sounds')
    assert response.status_code == 200
    assert response.is_json
    results = response.get_json()
    assert 'nature' in results
    for song in results['nature']:
        assert ".mp3" in song or ".wav" in song
