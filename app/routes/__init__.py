from flask import Blueprint
from app.routes import wallet

api = Blueprint('wallet', __name__)

api.add_url_rule('/v1/init', view_func=wallet.init_wallet, methods=['POST'])
api.add_url_rule('/v1/wallet', view_func=wallet.wallet, methods=['GET', 'POST', 'PATCH'])
api.add_url_rule('/v1/wallet/deposits', view_func=wallet.deposit_wallet, methods=['POST'])
api.add_url_rule('/v1/wallet/withdrawals', view_func=wallet.withdraw_wallet, methods=['POST'])
