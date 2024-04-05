import json, jwt
from flask import Blueprint, request, jsonify, current_app, Response
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime
#from auth_middleware import token_required
import random

from flask_cors import CORS
from model.users import User
from model.crypto import Transactions

import sqlite3

crypto_api = Blueprint('crypto_api', __name__,
                   url_prefix='/api/crypto')

dbURI = './instance/volumes/sqlite.db'
con = sqlite3.connect(dbURI)
cur = con.cursor()
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes 
CORS(app, origins=['*']) 


api = Api(crypto_api)

class CryptoAPI:        
    class transactions(Resource):  
        # @token_required
        #current_price = 2
        increase_factor = 0.05
        price_fluctuation_range = (0.5,2)
        
        res = cur.execute("SELECT current_price from crypto_price")
        current_price=res.fetchone()[0] 
        print("CURRENT_PRICE:"+str(current_price))     
        #print(type(current_price))  
        
        def price_adjustment(cls, transaction_type):
            if transaction_type == 'buy':
                cls.current_price *= (1 + cls.increase_factor)
            elif transaction_type == 'sell':
                cls.current_price *= (1 - cls.increase_factor)
        
            random_fluctuation = random.uniform(cls.price_fluctuation_range[0], cls.price_fluctuation_range[1])
            cls.current_price *= random_fluctuation 
            
            print("CURRENT PRICE: "+str(cls.current_price))
            
            con = sqlite3.connect(dbURI)
            cur = con.cursor()
            print("CRYPTO UPDATE CURRENT PRICE")
            sql="UPDATE crypto_price SET current_price = ?"
            print(type(cls.current_price))
            cur.execute(sql,(cls.current_price,))
            print("CRYPTO BEFORE COMMIT")
            con.commit()
        
        def calculate_profit(transaction_type, initial_price, final_price, amount):
            if transaction_type == 'buy':
                profit = (final_price - initial_price) * amount
            elif transaction_type == 'sell':
                profit = (initial_price - final_price) * amount
            else:
                profit = 0
            return profit
                                                    
                                    
        def post(self): # Create method
            try:
                body = request.get_json()
                if not body:
                    return {'message': 'Please provide transaction details'}, 400

                uid = body.get('uid')
                transaction_type = body.get('type')  # 'buy' or 'sell'
                amount = int(body.get('amount'))
                
                print(uid)
                print(transaction_type)
                print(amount)
                
                con = sqlite3.connect(dbURI)
                print("After connecting to db")
                cur = con.cursor()
                res = cur.execute("SELECT ifnull(sum(case transaction_type when 'buy' then amount else -amount END),0) FROM `transaction`")
                #print(len(res.fetchall()))
                total_crypto_coins=res.fetchone()[0]              
                #print(total_crypto_coins)
                
                print("CRYPTO1")
                print(total_crypto_coins)
                
                
                

                if not uid or not transaction_type or not amount:
                    return {'message': 'Incomplete transaction details'}, 400

                # Retrieve user
                user = User.query.filter_by(_uid=uid).first()
                if not user:
                    return {'message': 'User not found'}, 404
                
                print("SHEEEEEEEEEEEEESH")
                print(user.id)
                cur = con.cursor()
                res = cur.execute("SELECT ifnull(sum(case transaction_type when 'buy' then amount else -amount END),0) FROM `transaction` where user_id="+str(user.id))
                current_user_tokens=res.fetchone()[0] 
                print("USER TOKEN")
                print(current_user_tokens)
                
                if transaction_type == 'sell':
                    if current_user_tokens < amount:
                        return {'message': 'You are selling more than what u have and u are broke'}, 400
                    t = current_user_tokens- amount
                    print(t)
                else:
                    print("CALCUATE T")
                    t = current_user_tokens + amount
                    
                if t > 100:
                    return {'message': 'You are limited to only 100 coins'}, 400
                
                print("AFTER T")
                initial_price = self.current_price

                # Perform buy or sell transaction
                if transaction_type == 'buy':
                    if amount <= 0:
                        return {'message': 'Invalid amount for buying'}, 400
                    # Check if enough crypto available
                    if total_crypto_coins > 1000000:
                        return {'message': 'Exceeds available crypto limit'}, 400
                    # Adjust user's crypto balance
                    #user.crypto_balance += amount
                else:  # Transaction type is 'sell'
                    if amount <= 0:
                        return {'message': 'Invalid amount for selling'}, 400
                    # Check if user has enough crypto for selling
                    # Adjust user's crypto balance
                    
                # Adjust the price based on the transaction
                print("BEFORE adjustment")
                self.price_adjustment(transaction_type) #updates in the database
                #final_price = self.current_price

                # Calculate profit
                #profit = self.calculate_profit(transaction_type, initial_price, final_price, amount)

                # Save the updated user information
                
                p = Transactions(user.id,amount,transaction_type,self.current_price)
                p.create()

                return {
                    'message': f'{transaction_type.capitalize()} transaction successful',
                    'current_price_per_coin': self.current_price,
                    #'profit': profit
                }, 200

            except Exception as e:
                return {'message': 'Something went wrong', 'error': str(e)}
        
    
    
        def get(self): # Create method
                print("Hello Get")
                #body=request.get_json()
                #print(body)
                try:
                    #print("Hello Get 2")
                    con = sqlite3.connect(dbURI)
                    cur = con.cursor()
                    res = cur.execute("SELECT current_price FROM crypto_price")
                    current_price=res.fetchone()[0] 
                    print(current_price)             
                    return current_price                
                    
                except Exception as e:
                    print(e)
                    return {'message': 'Something went wrong', 'error': str(e)}
                             
    # building RESTapi endpoint
    api.add_resource(transactions, '/transactions')  