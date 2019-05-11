#https://github.com/kinecosystem/kin-sdk-python/tree/v2-master
from kin import KinClient, TEST_ENVIRONMENT
from kin import Keypair
from flask import Flask, request, jsonify, make_response

import sys
import os
import asyncio


#Variables for the environment
kin_env = TEST_ENVIRONMENT
unique_app_id = '1acd' #your app id assigned by Kin - you can use 1acd for testing
seed = os.environ['PRIVATE_KEY'] #private key (keep private/ store in .env file for production)
public_address = 'GCMVZ4B6P4QEZL727UH2A6ABA2AYY67GZC3NILDD2DVSZPRN4QQCRATG' #public key


app = Flask(__name__)


#function to handle http requests from the client
@app.route("/", methods=['GET','POST']) 
def message():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    if request.args.get("fund") is not None: #fund a newly created account
        response = loop.run_until_complete(fund_account(request.form.get("address"), request.form.get("memo"), float(request.form.get("amount"))))
    elif request.args.get("request") is not None: #send a payment to an account
        response = loop.run_until_complete(send_payment(request.form.get("address"), request.form.get("id"), request.form.get("memo"), float(request.form.get("amount"))))
    elif request.args.get("whitelist") is not None: #whitelist an account
        response = loop.run_until_complete(whitelist_transaction(request.data))
    else:
        response = make_response(jsonify({'error': 'no get vars'}), 500)
         
    loop.close() 
    return (response)


#consider placing try/catch blocks in the functions below to catch and return
#errors to your client

#initialize the kin object
#https://github.com/kinecosystem/kin-sdk-python/tree/v2-master#initialization
async def init_kin():
    client = KinClient(kin_env)
    account = client.kin_account(seed, app_id=unique_app_id)
    return client, account


 #Whitelists transactions so fees are zero
 #https://github.com/kinecosystem/kin-sdk-python/tree/v2-master#whitelist-a-transaction
async def whitelist_transaction(data):
    client, account = await init_kin()
    client_transaction = str(data, "utf-8")
    response = account.whitelist_transaction(client_transaction)
    await client.close()
    return response

#fund newly created account
#https://github.com/kinecosystem/kin-sdk-python/tree/v2-master#creating-a-new-account
async def fund_account(address,memo, amount):
    amount = min(amount,10) # set max we are willing to send - consider adding other security features
    client, account = await init_kin()
    minimum_fee = await client.get_minimum_fee() #they will charge 0 if whitelisted by Kin
    tx_hash = await account.create_account(address=address, starting_balance=amount, fee=minimum_fee, memo_text=memo)
    await client.close()
    return tx_hash

#send a payment
#https://github.com/kinecosystem/kin-sdk-python/tree/v2-master#sending-kin
async def send_payment(address,id, memo, amount):
    #you can use the id to record/authorise details of each user
    amount = min(amount,2) # set max we are willing to send - consider adding other security features
    client, account = await init_kin()
    minimum_fee = await client.get_minimum_fee() #they will charge 0 if whitelisted by Kin
    tx_hash = await account.send_kin(address=address, amount=amount, fee=minimum_fee, memo_text=memo)
    await client.close()
    return tx_hash


# Start listeining
if __name__ == "__main__":
    runport = int(os.environ.get("PORT", 5000)) 
    app.run(debug=False, host='0.0.0.0',port=runport)
