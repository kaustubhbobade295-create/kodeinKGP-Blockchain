import hashlib 
import time



# BLOCK STRUCTURE
# Each block stores its data and links to the previous block.


class Block:
    def __init__(self, index, data, previous_hash):
        self.index = index                  # Block number (0, 1, 2, ...)
        self.timestamp = time.time()        # Time when block was created
        self.data = data                    # The transaction or message stored in the block
        self.previous_hash = previous_hash  # Hash of the previous block (links the chain)
        self.nonce = 0                      # Nonce starts at 0, will be changed during mining
        self.hash = self.calculate_hash()   # The hash of this block


    # SHA-256 HASHING ALGORITHM
    # Combines all block info into one string, then hashes it
   

    def calculate_hash(self):
        # Joining all block fields into one big string
        block_string = (
            str(self.index) +
            str(self.timestamp) +
            str(self.data) +
            str(self.previous_hash) +
            str(self.nonce)
        )

        # sha256 needs bytes, so encoding the string first.
        return hashlib.sha256(block_string.encode()).hexdigest() #hexdigest converts the hash to a readable hexadecimal string.


   
    # MINING THE BLOCK USING PROOF OF WORK
    # Changing the nonce until the hash starts with enough zeros
    
    def mine_block(self, difficulty):
        # The target is a string of zeros, e.g. "0000" for difficulty 4
        target = "0" * difficulty

        print(f"\nMining block {self.index} with difficulty {difficulty} (target: '{target}...')...")

        start_time = time.time()  # Recording time when mining started

        # Trying different nonce values until we get a valid hash
        while not self.hash.startswith(target):
            self.nonce += 1                    # Trying next nonce
            self.hash = self.calculate_hash()  # Recalculating hash with new nonce

        time_taken = round(time.time() - start_time, 4)  # How long did it take?

        print(f"Nonce found : {self.nonce}")
        print(f"Hash        : {self.hash}")
        print(f"Time taken  : {time_taken} seconds")



# BLOCKCHAIN STRUCTURE
# A list of blocks linked together


class Blockchain:
    def __init__(self, difficulty=4):
        
        # ADJUSTABLE DIFFICULTY
        # we can pass any difficulty level when creating the blockchain.
        # Higher difficulty = more leading zeros required = longer mining time.
        # e.g. difficulty 2 needs "00...", difficulty 5 needs "00000..."
        
        self.difficulty = difficulty
        self.chain = []
        self.chain.append(self.create_genesis_block())  # First block is always calledthe genesis block


    
    # CHANGING DIFFICULTY ON THE FLY
    # We can call this anytime to make future blocks harder or easier to mine
    

    def set_difficulty(self, new_difficulty):
        print(f"\n>> Difficulty changed from {self.difficulty} to {new_difficulty}")
        self.difficulty = new_difficulty


    # GENESIS BLOCK
    # The very first block — has no previous block, so previous_hash is "0"


    def create_genesis_block(self):
        genesis = Block(0, "Genesis Block", "0")
        genesis.mine_block(self.difficulty)
        return genesis


    
    # ADDING A NEW BLOCK
    # Takes the previous block's hash and mines the new one
    

    def add_block(self, data):
        previous_block = self.chain[-1]               # Obtaining the last block in the chain
        new_block = Block(len(self.chain), data, previous_block.hash)
        new_block.mine_block(self.difficulty)         # Mining it with the current difficulty
        self.chain.append(new_block)                  # Adding to the chain


    
    # BLOCKCHAIN VALIDATION
    # Checking that all blocks are correctly linked and hashes are valid
    

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):           # Start from block 1 (skipping genesis)
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # condition 1: Does the block's stored hash match what we calculate now?
            if current_block.hash != current_block.calculate_hash():
                print(f"Block {i} has been tampered! Hash mismatch.")
                return False

            # condition 2: Does this block correctly point to the previous block?
            if current_block.previous_hash != previous_block.hash:
                print(f"Block {i} has broken link to previous block!")
                return False

        return True



# MAIN PROGRAM


if __name__ == "__main__":

    
    # DEMO 1: Starting with difficulty 2 (easy / fast)
    
    print("========== STARTING WITH DIFFICULTY 2 (Easy) ==========")
    my_blockchain = Blockchain(difficulty=2)

    my_blockchain.add_block("Rohan sends 10 BTC to Aman")
    my_blockchain.add_block("Aman sends 5 BTC to Vijay")

    
    # DEMO 2: Increasing difficulty to 4 (moderate)
    my_blockchain.set_difficulty(4)

    my_blockchain.add_block("Vijay sends 2 BTC to Ayan")
    my_blockchain.add_block("Ayan sends 1 BTC to Arin")

   
    # DEMO 3: Increasing difficulty to 5 (harder / slower)
    my_blockchain.set_difficulty(5)

    my_blockchain.add_block("Arin sends 0.5 BTC to Ojas")

   
    # PRINTING ALL BLOCKS
    print("\n\n========== FULL BLOCKCHAIN ==========")
    for block in my_blockchain.chain:
        print(f"\nBlock #{block.index}")
        print(f"  Data          : {block.data}")
        print(f"  Nonce         : {block.nonce}")
        print(f"  Previous Hash : {block.previous_hash}")
        print(f"  Hash          : {block.hash}")


    # VALIDATING THE CHAIN
    print("\n\n========== VALIDATION ==========")
    if my_blockchain.is_chain_valid():
        print("Blockchain is VALID. All blocks are intact.")
    else:
        print("Blockchain is INVALID. Something went wrong.")

    
    # TAMPER DEMO/ ALTERATING A BLOCK TO SHOW VALIDATION FAILURE
    print("\n\n========== TAMPER TEST ==========")
    print("Trying to change Block 1's data secretly...")
    my_blockchain.chain[1].data = "Rohan sends 1000 BTC to Hacker"

    if my_blockchain.is_chain_valid():
        print("Blockchain is VALID.")
    else:
        print("Blockchain is INVALID — tampering detected! The chain is broken.")
