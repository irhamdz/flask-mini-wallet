import datetime
import uuid

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import (BOOLEAN, INTEGER, TEXT, TIMESTAMP,
                                            UUID, VARCHAR)
from sqlalchemy.orm import relationship

db = SQLAlchemy()
migrate = Migrate()


class Account(db.Model):
    __tablename__ = 'account'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_xid = db.Column(VARCHAR(256), nullable=False)
    token = db.Column(VARCHAR(256), unique=True)
    wallet = relationship("Wallet", uselist=False, backref="account")


class Wallet(db.Model):
    __tablename__ = 'wallet'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    balance = db.Column(INTEGER, default=0)
    id_account = db.Column(UUID(as_uuid=True), db.ForeignKey('account.id'), nullable=False)
    enabled = db.Column(BOOLEAN, default=False)
    enabled_at = db.Column(TIMESTAMP, default=datetime.datetime.utcnow)


class WalletHistory(db.Model):
    __tablename__ = 'wallet_history'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id_wallet = db.Column(UUID(as_uuid=True), db.ForeignKey('wallet.id'), nullable=False)
    amount = db.Column(INTEGER, nullable=False)
    action = db.Column(INTEGER, nullable=False)
    action_by = db.Column(UUID(as_uuid=True), db.ForeignKey('account.id'), nullable=False)
    action_at = db.Column(TIMESTAMP, default=datetime.datetime.utcnow)
    ref_id = db.Column(TEXT, nullable=False)
