from app.models import Account
from app.util import generate_token


def test_new_account(app):
    token = generate_token()
    account = Account(customer_xid='ea0212d3-abd6-406f-8c67-868e814a2436', token=token)
    assert account.customer_xid == 'ea0212d3-abd6-406f-8c67-868e814a2436'
    assert account.token == token
