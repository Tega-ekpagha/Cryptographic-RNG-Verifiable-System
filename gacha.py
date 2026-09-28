# %%
## Gacha Game Implementation
#Three tiers are used Common, Legendary and Rare
import hmac 
import hashlib 
import secrets 

# %%

class GachaSystem:
    def __init__(self):
 # 
#This system utilises HARD-PITY mechanics
#Hard-coded at the 90th consecutive pull without a "Legendary" item the system will force a "Legendary" pull

#DECLARED TIERS
        self.RARITY_TIERS = [
            ("Legendary", 1),
            ("Rare",  25),
            ("Common", 74),
        ] 
        self.HARD_PITY = 90

    

    def get_drop_rates(self):
        return {tier: chance for tier,chance in self.RARITY_TIERS}

    def get_hard_pity(self):
        return self.HARD_PITY

#Mapping the HMAC-SHA256 hash to the rarity tiers


#Mathematical formulation:

##HMAC-SHA256 output is converted to a fair 0-9999 basis-point roll
##The first 8-hex characters are taken (32 bits)
##The division 2^32 is implemented 
## The result is multiplied by 10000 to get a 0-9999 basis-point

    def _hash_to_roll(self, outcome_hash):

        hash_int       = int(outcome_hash[:8], 16)
        provable_float = hash_int / (2**32)       # maps to [0.0, 1.0)
        return int(provable_float * 10000)        # maps to [0, 9999]



    # Hard pity mechanics: encoded that at the 90th pull a "Legendary" pull is guaranteed
    def rarity_outcome(self, outcome_hash, legendary_pity_counter=0):

        roll = self._hash_to_roll(outcome_hash)
        if legendary_pity_counter >= self.HARD_PITY - 1:
            return "Legendary", roll, True, 0

    #For rarity outcomes outside of "Legendary",
        #They are mapped against the 0-9999 basis roll
        #The chance is multiplied by 100 e.g. Common 74*100= 7400
        #Mapped against the roll e.g.2300 < 7400
        #The counter updates until or unless a "Legendary" roll is hit

        base = 0
        for tier, chance in self.RARITY_TIERS:
            base += chance * 100
            if roll < base:
                updated_counter = 0 if tier == "Legendary" else legendary_pity_counter + 1
                return tier, roll, False, updated_counter

        return "Common", roll, False, legendary_pity_counter + 1


