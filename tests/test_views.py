def test_homepage(client):
    response = client.get('/')
    assert response.status_code == 200


def test_sounds(client):
    response = client.get('/sounds')
    assert response.status_code == 200
    assert response.is_json
    results = response.get_json()
    for song in results:
        assert ".mp3" in song or ".wav" in song
