import datetime
from http import HTTPStatus

from app import util
from app.constants import DEPOSIT, DISABLED, ENABLED, ERROR, FAIL, SUCCESS, WITHDRAW
from app.models import Account, Wallet, WalletHistory, db
from flask import jsonify, request


def init_wallet():
    """
    Init wallet for a customer

    Param:
        - customer_xid (varchar): customer id
    Return:
        {
            "data": {
                "token": "cb04f9f26632ad602f14acef21c58f58f6fe5fb55a"
            },
            "status": "success"
        }
    """
    # default value
    status = SUCCESS
    resp_data = ""
    status_code = HTTPStatus.OK

    # get form body
    customer_id = request.form.get('customer_xid')
    if customer_id is None:
        return util.jsend_response(ERROR, "customer_xid is required!", HTTPStatus.BAD_REQUEST)

    account = Account.query.filter_by(customer_xid=customer_id).first()
    if account:
        # check if wallet for account is exist
        wallet = Wallet.query.filter_by(id_account=account.id).first()
        if not wallet:
            util.create_wallet(account)

        # check if token exist
        if account.token:
            resp_data = {
                "token": account.token
            }
        else:
            account.token = util.generate_token()
            try:
                db.session.commit()
                resp_data = {
                    "token": account.token
                }
            except Exception as e:
                status = FAIL
                resp_data = e
                status_code = HTTPStatus.BAD_REQUEST

    else:
        token = util.generate_token()
        account = Account(customer_xid=customer_id, token=token)
        db.session.add(account)
        try:
            db.session.commit()

            # create wallet
            util.create_wallet(account)

            resp_data = {
                "token": account.token
            }
        except Exception as e:
            status = FAIL
            resp_data = e
            status_code = HTTPStatus.BAD_REQUEST

    return util.jsend_response(status, resp_data, status_code)


def wallet():
    """
    View wallet balance / enable or disable wallet,
    disable wallet will return fail

    Param:
        - Token (varchar): account token
        - is_disabled (bool): for disabling wallet (optional)

    Return:
    - wallet balance:
        {
            "data": {
                "wallet": {
                    "balance": 0,
                    "enabled_at": "Sat, 04 Dec 2021 09:45:52 GMT",
                    "id": "b4b48a7c-2553-4428-8426-2aa568a6ca93",
                    "owned_by": "a44301bf-c018-4311-8bde-df6ec1995aa7",
                    "status": "enabled"
                }
            },
            "status": "success"
        }

    - enable wallet:
        {
            "data": {
                "wallet": {
                    "balance": 0,
                    "enabled_at": "Sat, 04 Dec 2021 09:45:52 GMT",
                    "id": "b4b48a7c-2553-4428-8426-2aa568a6ca93",
                    "owned_by": "a44301bf-c018-4311-8bde-df6ec1995aa7",
                    "status": "enabled"
                }
            },
            "status": "success"
        }

    - disable wallet:
        {
            "data": {
                "wallet": {
                    "balance": 0,
                    "enabled_at": "Sat, 04 Dec 2021 09:45:52 GMT",
                    "id": "b4b48a7c-2553-4428-8426-2aa568a6ca93",
                    "owned_by": "a44301bf-c018-4311-8bde-df6ec1995aa7",
                    "status": "disabled"
                }
            },
            "status": "success"
        }
    """
    auth_token = request.headers.get('Authorization')
    is_disabled = request.form.get('is_disabled')
    if auth_token is None:
        return util.jsend_response(ERROR, "token is missing or not found", HTTPStatus.FORBIDDEN)
    splitted_token = auth_token.split()
    token = splitted_token[1]

    # check token
    account = Account.query.filter_by(token=token).first()
    if not account:
        return util.jsend_response(ERROR, "token is missing or not found", HTTPStatus.FORBIDDEN)
    else:
        wallet = account.wallet

    success_data = {
        "wallet": {
            "id": wallet.id,
            "owned_by": wallet.id_account,
            "status": ENABLED if wallet.enabled else DISABLED,
            "enabled_at": wallet.enabled_at if wallet.enabled else None,
            "balance": wallet.balance
        }
    }
    if request.method == 'GET':
        # view wallet balance
        if not wallet.enabled:
            return util.jsend_response(ERROR, "wallet is not enabled", HTTPStatus.FORBIDDEN)

        return util.jsend_response(SUCCESS, success_data)
    elif request.method == 'POST':
        # enable wallet
        if wallet.enabled:
            return util.jsend_response(ERROR, "wallet already enabled", HTTPStatus.BAD_REQUEST)
        else:
            wallet.enabled = True
            wallet.enabled_at = datetime.datetime.utcnow()
            db.session.commit()

            success_data["wallet"]["status"] = ENABLED if wallet.enabled else DISABLED
            success_data["wallet"]["enabled_at"] = wallet.enabled_at if wallet.enabled else None
            return util.jsend_response(SUCCESS, success_data)
    else:
        # disabled wallet
        if not wallet.enabled:
            return util.jsend_response(ERROR, "wallet is not enabled", HTTPStatus.BAD_REQUEST)
        else:
            if is_disabled:
                wallet.enabled = False
                db.session.commit()
            else:
                pass

            success_data["wallet"]["status"] = ENABLED if wallet.enabled else DISABLED
            success_data["wallet"]["enabled_at"] = wallet.enabled_at
            return util.jsend_response(SUCCESS, success_data)


def deposit_wallet():
    """
    Deposit wallet endpoint

    Param:
        - Token (varchar): account token
    
    Return:
        {
            "data": {
                "deposit": {
                    "amount": 100000,
                    "deposited_at": "Sat, 04 Dec 2021 11:49:08 GMT",
                    "deposited_by": "a44301bf-c018-4311-8bde-df6ec1995aa7",
                    "id": "25cfe233-495a-4610-b4f4-9c01642e1bd8",
                    "reference_id": "50535246-dcb2-4929-8cc9-91893810938",
                    "status": "success"
                }
            },
            "status": "success"
        }
    """
    auth_token = request.headers.get('Authorization')
    amount = request.form.get('amount', 0)
    reference_id = request.form.get('reference_id')
    if auth_token is None:
        return util.jsend_response(ERROR, "token is missing or not found", HTTPStatus.FORBIDDEN)

    splitted_token = auth_token.split()
    token = splitted_token[1]

    # check token
    account = Account.query.filter_by(token=token).first()
    if not account:
        return util.jsend_response(ERROR, "token is missing or not found", HTTPStatus.FORBIDDEN)
    else:
        wallet = account.wallet

    # check is wallet enabled
    if not wallet.enabled:
        return util.jsend_response(ERROR, "wallet is not enabled", HTTPStatus.FORBIDDEN)

    # check ref id
    ref_id_exist = WalletHistory.query.filter_by(ref_id=reference_id).first()
    if ref_id_exist:
        return util.jsend_response(ERROR, "reference id already exist", HTTPStatus.BAD_REQUEST)

    # deposit
    wallet.balance += float(amount)
    db.session.commit()

    # create deposit history
    history = WalletHistory(
        id_wallet=wallet.id,
        amount=amount,
        action=DEPOSIT,  # action = 1 is deposit
        action_by=account.id,
        ref_id=reference_id
    )
    db.session.add(history)
    db.session.commit()

    success_data = {
        "deposit": {
            "id": history.id,
            "deposited_by": history.action_by,
            "status": "success",
            "deposited_at": history.action_at,
            "amount": history.amount,
            "reference_id": history.ref_id
        }
    }

    return util.jsend_response(SUCCESS, success_data)


def withdraw_wallet():
    """
    """
    auth_token = request.headers.get('Authorization')
    amount = request.form.get('amount', 0)
    reference_id = request.form.get('reference_id')
    if auth_token is None:
        return util.jsend_response(ERROR, "token is missing or not found", HTTPStatus.FORBIDDEN)

    splitted_token = auth_token.split()
    token = splitted_token[1]

    # check token
    account = Account.query.filter_by(token=token).first()
    if not account:
        return util.jsend_response(ERROR, "token is missing or not found", HTTPStatus.FORBIDDEN)
    else:
        wallet = account.wallet

    # check is wallet enabled
    if not wallet.enabled:
        return util.jsend_response(ERROR, "wallet is not enabled", HTTPStatus.FORBIDDEN)

    # check ref id
    ref_id_exist = WalletHistory.query.filter_by(ref_id=reference_id).first()
    if ref_id_exist:
        return util.jsend_response(FAIL, "reference id already exist", HTTPStatus.BAD_REQUEST)

    # check if balance bigger than amount withdraw
    if wallet.balance < float(amount):
        return util.jsend_response(FAIL, "amount is bigger than wallet balance", HTTPStatus.BAD_REQUEST)

    # withdraw
    wallet.balance -= float(amount)
    db.session.commit()

    # create deposit history
    history = WalletHistory(
        id_wallet=wallet.id,
        amount=amount,
        action=WITHDRAW,  # action = 1 is deposit
        action_by=account.id,
        ref_id=reference_id
    )
    db.session.add(history)
    db.session.commit()

    success_data = {
        "deposit": {
            "id": history.id,
            "withdrawn_by": history.action_by,
            "status": "success",
            "withdrawn_at": history.action_at,
            "amount": history.amount,
            "reference_id": history.ref_id
        }
    }

    return util.jsend_response(SUCCESS, success_data)
