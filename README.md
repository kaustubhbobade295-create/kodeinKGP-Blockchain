# kodeinKGP-Blockchain
Implementing Proof Of Work and SHA-256 algorithm

The task was to create a blockchain using proof of work and SHA-256 algorithm.The language used was python.Below are the complete details regarding the project.

#How Blocks are created?
Each block is created using the Block class. When a new block is created, it is given:
Index — the block's position in the chain (0, 1, 2, ...)
Timestamp — the exact time the block was created using time.time()
Data — the transaction message stored in the block I(Rohan send 10 btc to aman)
Previous Hash — the hash of the block before it, which links the chain together
Nonce — starts at 0 and gets incremented during mining
Hash — calculated immediately when the block is created using SHA-256
The very first block is called the Genesis Block. Since there is no block before it, its previous hash is set to "0"


#How hashing works?
Hashing is done using the SHA-256 algorithm from Python's built-in hashlib library.
All the block's fields are joined into one single string:
block_string = index + timestamp + data + previous_hash + nonce
This string is then passed through SHA-256:
"pythonhashlib.sha256(block_string.encode()).hexdigest()"
The result is a fixed-length 64-character hexadecimal string like:
0000ab23f91d7c3e2b4a...
Key property of hashing: If even one character of the block's data changes, the entire hash changes completely. This is what makes tampering/altering detectable.


How proof of mining works?
Mining is the process of finding a valid hash for a block. A hash is considered to be valid only if it starts with a certain number of zeros — this is called the difficulty condition.
The mining function works like this:

Start with nonce = 0
Calculate the block's hash
Check if the hash starts with the required number of zeros
If not — increment the nonce by 1 and recalculate
Keep repeating until a valid hash is found

python Code:
"while not self.hash.startswith(target):
    self.nonce += 1
    self.hash = self.calculate_hash()"

This is pure brute force — the miner just keeps trying different nonce values until it gets lucky and lands on a valid hash. This is exactly how Bitcoin mining works.


Purpose of nonce values?
The nonce (Number Only Used Once) is the key variable that the miner changes during mining.
Since all other fields of a block (index, timestamp, data, previous hash) are fixed, the nonce is the only thing the miner can change to get a different hash output.
By incrementing the nonce by 1 each attempt, the miner keeps producing completely different hashes until one satisfies the difficulty condition. The final nonce value that produced the valid hash is stored permanently inside the block.


#How blockchain validation is implemented?
The is_chain_valid() function loops through every block in the chain and runs two conditions on each:
Condition 1 — Hash Integrity:
Recalculates the block's hash from scratch and compares it to the hash stored inside the block. If they don't match, the block's data has been tampered with.
python:
"if current_block.hash != current_block.calculate_hash():"
    # Block has been tampered

Condition 2 — Chain Linkage:
Checks that the current block's previous_hash actually matches the real hash of the block before it. If someone tampers with a block, its hash changes — which breaks this link for the next block.
python:
"if current_block.previous_hash != previous_block.hash:"
    # Chain link is broken

If both checks pass for every block, the chain is valid. If either check fails on any block, tampering is detected immediately.


#Why increasing difficulty increases mining time?
Since SHA-256 produces essentially random output, the probability of getting a hash that starts with the required zeros decreases exponentially as difficulty increases:
This means the miner has to try far more nonce values at higher difficulty, which directly increases the time taken to mine a block. You can observe this clearly in the output — blocks mined at difficulty 5 take noticeably longer than blocks mined at difficulty 2.

example:
Difficulty 2 → 1 in 256 hashes will be valid on average
Difficulty 4 → 1 in 65,536 hashes will be valid on average
Difficulty 6 → 1 in 16,777,216 hashes will be valid on average


#Features Implemented:

-Block structure with index, timestamp, data, previous hash, nonce, and current hash
-SHA-256 hashing
-Proof of Work mining with nonce increment loop
-Genesis block creation
-Linking blocks via previous hash
-Blockchain validation (hash integrity + chain linkage checks)
-Tamper detection demo
-Adjustable mining difficulty (bonus feature)


#Tech Stack:

Language: Python 3
Libraries: hashlib (built-in), time (built-in)
