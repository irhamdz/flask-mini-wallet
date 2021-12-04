def test__view_disabled_wallet(client):
    response = client.get('/api/v1/wallet')
    assert response.status_code == 403
    assert b"Welcome to miniwallet!" in response.data


