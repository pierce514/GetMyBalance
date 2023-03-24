import os
from flask import Flask, jsonify, render_template, request
from web3 import Web3, HTTPProvider

# Replace with your own Alchemy API key
ALCHEMY_API_KEY = "-_Q4IYd85zziucxcqDVVB4WoAAqgZrmd"
ETHEREUM_NODE_URL = f"https://polygon-mainnet.g.alchemy.com/v2/{ALCHEMY_API_KEY}"

web3 = Web3(HTTPProvider(ETHEREUM_NODE_URL))

# Address to query
ADDRESS = "0xbed0BCEa9c75d3E34D0E4afF2146249F0aa08916"

# ERC-20 ABI
TOKEN_ABI = [
    {
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "type": "function",
    }
]


app = Flask(__name__)

def get_matic_balance(address):
    try:
        contract = web3.eth.contract(address=address, abi=TOKEN_ABI)
        decimals = contract.functions.decimals().call()
        balance = contract.functions.balanceOf(address).call()
        formatted_balance = balance / (10 ** decimals)
        return formatted_balance, None
    except Exception as e:
        return None, str(e)

@app.route('/balance', methods=['GET'])
def get_balance():
    address = request.args.get('address')
    if address and Web3.is_address(address):
        ADDRESS = Web3.to_checksum_address(address)
        balance, error = get_matic_balance(ADDRESS)
        if balance is not None:
            return jsonify({'balance': balance})
        else:
            return jsonify({'error': error}), 500
    else:
        return jsonify({'error': 'Invalid address'}), 400

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
