def test__home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome to miniwallet!" in response.data
