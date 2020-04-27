# A py script for study some blockchain principles based in: https://developer.ibm.com/technologies/blockchain/tutorials/develop-a-blockchain-application-from-scratch-in-python/
from hashlib import sha256
import json
import time


class Block:
    def __init__(self, index, transactions, timestamp, previous_hash):
        # index = unique id of blocks
        # transactions = list of data
        # timestamp = time of generation of the block
        # previous_hash = the hash of previous element for keep blocks connected
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp

    # hash function is a function that takes data of any size and produce data of a fixed size (a hash)
    # is generally used to identify the input
    # characteristics of a hash: 
        # 1 - It should be easy to compute
        # 2 - It should be deterministic, meaning the same data will always result in the same hash
        # 3 - It should be uniformly random, meaning even a single bit change in the data should change the hash significantly
    # Because of theses characteristics
        # 1 - It is virtually impossible to guess the input data given the hash.
        # 2 - If you know both the input and the hash, you can simply pass the input through the hash function to verify the provided hash
    def compute_hash(block):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()
    
    def add_block(self, block, proof):
        # verification includes: 
            # 1 - Checking if the proof is valid; 
            # 2 - The previous hash referred in the block and the hash of the lastest block in the chain match.
        previous_hash = self.last_block.hash
        if previous_hash != block.previous_hash:
            return False
        if not Blockchain.is_valid_proof(block, proof):
            return False
        # if it pass in verification, add the block into the chain
        block.hash = proof
        self.chain.append(block)
        return True
    
    def is_valid_proof(self, block, block_hash):
        # check if block_hash is valid hash of block and satisfies the difficulty criteria
        return (block_hash.startswith('0' * Blockchain.difficulty) and block_hash == block.compute_hash())


# if the content of any previous blocks changes
    # 1 - The hash of that previous block would change
    # 2 - This will lead to a mismatch with the previous_hash field
    # 3 - since the input data to compute the hash of any block also consists of the previous_hash field, the hash of the next block will also change
class Blockchain:
    # difficulty of proof of work algorithm
    difficulty = 2

    def __init__(self, nonce):
        self.chain = []
        self.create_genesis_block()
        # nonce is a number that we can keep on changin until we get a hash that satisfies our constrain
        self.nonce = nonce
    
    # create the first block of the blockchain
    # the block has index 0, previous_hash as 0 and a valid hash
    def create_genesis_block(self):
        genesis_block = Block(0, [], time.time(), "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    # retrieve the most recent block in the chain.
    # Note that the chain will always consist of at least one block.
    @property
    def last_block(self):
        return self.chain[-1]
    
    # If we change the previous block, the hashes of all the blocks that follow can be re-computed quite easily to create a different valid blockchain
    # To prevent this, we use the asymmetry in efforts of hash functions to make the task of calculating the hash difficult and random
        # Instead of accepting any hash for the block, we add some constrain to it.
        # To do this we use the nonce. -> This technique is a simplified version of the Hashcash algorithm used in bitcoin.
        # proof of work is difficult to compute but very easy to verify once you figure out the nonce
    def proof_of_work(self, block):
        block.nonce = 0
        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()
        return computed_hash

    
