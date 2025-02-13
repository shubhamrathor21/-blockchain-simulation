import hashlib
import time
import json
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

class Block:
    def __init__(self, index, transactions, previous_hash, difficulty=2):
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0
        self.difficulty = difficulty
        self.hash = self.mine_block()
    
    def compute_hash(self):
        block_data = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_data.encode()).hexdigest()
    
    def mine_block(self):
        """Basic Proof-of-Work: Find a hash with leading 'difficulty' zeros."""
        while True:
            hash_value = self.compute_hash()
            if hash_value[:self.difficulty] == "0" * self.difficulty:
                return hash_value
            self.nonce += 1

class Blockchain:
    def __init__(self, difficulty=2):
        self.chain = []
        self.difficulty = difficulty
        self.create_genesis_block()
    
    def create_genesis_block(self):
        """Creates the first block (Genesis Block)."""
        genesis_block = Block(0, "Genesis Block", "0", self.difficulty)
        self.chain.append(genesis_block)
    
    def add_block(self, transactions):
        """Adds a new block to the blockchain."""
        previous_block = self.chain[-1]
        new_block = Block(len(self.chain), transactions, previous_block.hash, self.difficulty)
        self.chain.append(new_block)
    
    def is_chain_valid(self):
        """Validates the blockchain integrity."""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            if current_block.hash != current_block.compute_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True

    def get_chain(self):
        return [{
            "index": block.index,
            "timestamp": block.timestamp,
            "transactions": block.transactions,
            "previous_hash": block.previous_hash,
            "hash": block.hash,
            "nonce": block.nonce
        } for block in self.chain]

blockchain = Blockchain(difficulty=3)

@app.route('/chain', methods=['GET'])
def get_chain():
    return jsonify(blockchain.get_chain())

@app.route('/add_block', methods=['POST'])
def add_block():
    data = request.json.get("transactions", "No transaction data")
    blockchain.add_block(data)
    return jsonify({"message": "Block added successfully!"})

@app.route('/validate', methods=['GET'])
def validate_chain():
    return jsonify({"valid": blockchain.is_chain_valid()})

if __name__ == '__main__':
    app.run(debug=True)
