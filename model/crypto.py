from random import randrange
from datetime import datetime
import os
import base64
import json

from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

class Transactions(db.Model):
    __tablename__ = 'transaction'
    
    transaction_id = db.Column(db.Float,primary_key=True)
    user_id = db.Column(db.Float, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    transaction_type = db.Column(db.String(50), nullable=False)
    executed_price = db.Column(db.Float, nullable=False)


    def __init__(self,user_id, amount, transaction_type,executed_price):
        self.user_id = user_id
        self.amount = amount
        self.transaction_type = transaction_type
        self.executed_price = executed_price

    def create(self):
        try:
            print(self.user_id)
            print(self.amount)

            db.session.add(self)
            db.session.commit()
            return self
        except IntegrityError:
            db.session.remove()
            return None


def init_data():
    with app.app_context():
        
        db.create_all()

        transactions = [
            Transactions(uid='azeemK', amount=10.5, transaction_type='buy'),
            Transactions(uid='ahadB', amount=5.2, transaction_type='sell'),
            Transactions(uid='akshatP', amount=8.7, transaction_type='buy')
            # Add more transactions as needed
        ]

        for transaction in transactions:
            try:
                transaction.create()
            except IntegrityError:
                db.session.remove()
                print(f"Failed to create transaction: {transaction}")


#if __name__ == "__main__":
    #init_data()