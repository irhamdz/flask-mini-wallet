from app.models import Account


def test__missing_token(client):
    response = client.get('/api/v1/wallet', headers={'Authorization': 'Token iahdiahidhidahiad'})
    assert response.status_code == 403
    assert b"token is missing or not found" in response.data


def test__view_balance(client):
    account = Account.query.first()
    response = client.get('/api/v1/wallet', headers={"Authorization": f"Token {account.token}"})
    assert response.status_code == 200
    assert b"balance" in response.data
