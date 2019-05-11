# Kin Unity SDK tutorial-server
This is a simple server side implementation of  [Kin's python SDK](https://github.com/kinecosystem/kin-sdk-python/tree/v2-master). It can work as a standalone implementation, or together with the client side wrapper provided in the [Kin Unity SDK tutorial](https://github.com/hitwill/kin-sdk-unity-tutorial/tree/master).

With this code, you can call [Kin's blockchain](https://www.kin.org/blockchainExplorer) to:
1. Fund newly created accounts
2. Send payments
3. Whitelist transactions for the client

You can also extend it to suit your needs.

## Installation

1. Clone to your localhost directory
2. Use [pip](https://stackoverflow.com/questions/7225900/how-to-install-packages-using-pip-according-to-the-requirements-txt-file-from-a) to install dependencies in requirements.txt
3. Modify the following variables in server.py
```
kin_env = TEST_ENVIRONMENT
unique_app_id = '1acd' #your app id assigned by Kin - you can use 1acd for testing
seed = os.environ['PRIVATE_KEY'] #private key (keep private/ store in .env file for production)
public_address = 'GCMVZ4B6P4QEZL727UH2A6ABA2AYY67GZC3NILDD2DVSZPRN4QQCRATG' #public key
```

You can use [Kin's Laboratory](https://laboratory.kin.org/index.html#account-creator?network=test) to generate your seed and public address.

4. Push to your server (Heroku recommended)


## Usage
Simply call the server with GET/POST to perform the following functions:
1. [Fund a new account](https://github.com/kinecosystem/kin-sdk-python/tree/v2-master#creating-a-new-account)

    GET: fund = 1

   POST: address, memo, amount

2. [Send a payment to an account](https://github.com/kinecosystem/kin-sdk-python/tree/v2-master#sending-kin)
  
   GET: request = 1

   POST: address, id, memo, amount

3. [Whitelist a transaction for the client](https://github.com/kinecosystem/kin-sdk-python/tree/v2-master#whitelist-a-transaction)

   GET: whitelist = 1

   POST: address, id, memo, amount

#### Variables
1. **address:** The blockchain address you wish to make a payment to
2. **memo:** Memo to add to your transaction
3. **amount:** Amount to send for your transaction
4. **id:** A unique id for your client (optional)

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details.



## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

