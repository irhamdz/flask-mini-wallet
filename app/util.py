from http import HTTPStatus
import random
import time
import uuid
from flask.json import jsonify
from app.constants import FAIL, SUCCESS

from app.models import Account, Wallet, db


def generate_token():
    """Generate a token by random string"""
    token = random_string()

    # check unique token on db
    meeting_code_exists = Account.query.filter_by(token=token).scalar() is not None
    while meeting_code_exists:
        token = random_string()

    return token


def random_string():
    """generate a random string by merge from mili second and uuid"""
    milsec = repr(time.time()).replace(".", "")[-6:]
    ranuuid = str(uuid.uuid4()).replace("-", "")[:10]

    result = ranuuid + milsec

    generated_uid = ''.join(random.sample(result, len(result)))

    return generated_uid


def create_wallet(account):
    """
    Create a wallet for an account

    Param:
        - account (sqlalchemyobj): account obj
    
    Response:
        - wallet (sqlalchemyobj): wallet obj
    """
    wallet = Wallet(id_account=account.id)
    try:
        db.session.add(wallet)
        db.session.commit()
    except Exception as e:
        return e
    return wallet


def jsend_response(status, message, status_code=HTTPStatus.OK):
    """
    http response based on jsend response

    Param:
        - status (string): status string
        - message (any): message of response
        - status_code (http_status): http status code
    
    #TODO: complete this!
    Return:
        - status = "success":
        {

        }
    """
    response = {}
    if status in [SUCCESS, FAIL]:
        response = jsonify(status=status, data=message), status_code
    else:
        response = jsonify(status=status, message=message), status_code

    return response
