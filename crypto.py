import hmac 
import hashlib 
import secrets 

class CryptoSystem:
    def __init__(self):
        pass 

    def generate_server_seed(self):
        #Generate a random 32 byte server seed
        return secrets.token_hex(32) 

    def generate_hashed_server_seed(self, server_seed):
        # The operator provides the user with a hashed version  server seed
        return hashlib.sha256(server_seed.encode()).hexdigest() 

    def generate_client_seed(self):
        #INPUT PHASE
        
        #Player input is required for the client seed to be generated
        message = input("Please provide an input to generate your own secret seed, if left blank the system will generate one.") 
        if not message:
            return secrets.token_hex(32) 
        return hashlib.sha256(message.encode()).hexdigest() 

    #Seeds are concatenated and then hashed to produce the final hash
    
    def generate_final_hash(self, server_seed, client_seed, nonce=0):
        #Generate the final hashed outcome here with HMAC-SHA256
        message = f"{client_seed}:{nonce}".encode() 
        return hmac.new(server_seed.encode(), message, hashlib.sha256).hexdigest() 

    def verify_commitment(self, server_seed, commitment_hash):
        #Provided the server seed has not been tampered with, the commitment hash should 
        #match the recalculated hash of the server seed
        recalculated = hashlib.sha256(server_seed.encode()).hexdigest()  
        valid = hmac.compare_digest(recalculated, commitment_hash) 
        if valid:
            print("Verification successful: Your loot outcome is fair and has not been tampered with.") 
        else:
            print("Warning: Verification failed, this could indicate tampering or an error in the process.") 
        return valid

