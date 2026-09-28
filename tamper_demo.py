from crypto import CryptoSystem
from gacha import GachaSystem

class GameSession:
    def __init__(self):
        self.crypto = CryptoSystem()
        self.gacha = GachaSystem()

    def run_session(self, num_pulls=10):


        #COMMITMENT PHASE
        opening = """
                                        ======================================================================
                                                                --- COMMITMENT PHASE ---
                                        ======================================================================

               This system uses a provably fair scheme, to ensure that the gacha pull is fair and transparent to all our players.
               Before your transaction begins, the system will explain some terms. 

         * Hard Pity is a mechanic used in our system that helps players achieve a legendary items, if after a set number of pulls,
         a legendary item is yet to be revealed.'

        * A server seed is what the system uses to help with our gacha pull mechanics. 

        * With a server seed we can generate a commitment, which is a hashed version of the server seed.
        
        * Player input is needed to generate your client seed, should this be left blank the server will provide a randomised input.

       
              The generated commitment will be displayed before the gacha pull and is used to verify that the server seed has not been tampered with. 
              This verification checks that the odds of receiving your item after you pulled your roll was not altered after the gacha pull is completed.

              This scheme is being used to improve player trust in our systems. A full audit script will be displayed to
              make explicit that all loot box item odds were not altered after the player gacha pull was computed.

                    
              In this audit, the server seed is revealed, and there will be further instructions on how to 
              externally verify the results with an industry-verified independent party.

                    
        """
        print(opening)
        print("The system has begun the gacha pull process. Please wait while we generate the server seed and commitment.")

        server_seed = self.crypto.generate_server_seed()
        commitment = self.crypto.generate_hashed_server_seed(server_seed)
        
        display_drop_rates = self.gacha.get_drop_rates()
        display_pity_rate = self.gacha.get_hard_pity()
        
        print("The following drop rates are now being displayed for this gacha pull:")
        for rarity, rate in display_drop_rates.items():
            print(f"{rarity}: {rate}%")

        print(f"\nA Hard Pity Mechanic is implemented in this system at {display_pity_rate} pulls.")
        print(f"\nAt {display_pity_rate} a Legendary item will be pulled automatically if after this set amount a Legendary is still yet to be pulled.")
        print(f"The Commitment for this session is: {commitment}\n")

        #INPUT PHASE -- The client seed is set ONCE per session, not once per pull
        print("The system is now ready for your input")
        client_seed = self.crypto.generate_client_seed()
        print(f"Your client seed is {client_seed}. This seed will be used for every pull in this session.\n")


        ##ROLL PHASE 
        
        
        
        pity_counter = 0
        results = []
        #Empty list to display session stats to the player

        for pull_number in range(1, num_pulls + 1):
            final_hash = self.crypto.generate_final_hash(server_seed, client_seed, nonce=pull_number)
            tier, roll, pity_triggered, pity_counter = self.gacha.rarity_outcome(final_hash, pity_counter)

            results.append({
                "pull": pull_number,
                "hash": final_hash,
                "roll": roll,
                "tier": tier,
                "pity_triggered": pity_triggered,
            })

            pity_note = "  <-- HARD PITY TRIGGERED" if pity_triggered else ""
            print(f"Pull {pull_number:>3}: roll={roll:>4}/9999  ->  {tier}{pity_note}")



        ##VERIFICATION PHASE
        
        
        print("\n======================================================================")
        print("                      --- VERIFICATION PHASE ---")
        print("======================================================================")
        print("To ensure absolute transparency, this system provides both an automatic")
        print("internal check and the data needed for independent verification, with third-party authorities.\n")
        
        print(f"Raw Server Seed Revealed: {server_seed}")
        print(f"Your Client Seed:         {client_seed}")
        print(f"Original Commitment:      {commitment}\n")
        
      # 1. Internal System Verification
        print("--- 1. INTERNAL SYSTEM VERIFICATION ---")
        

        print("[!] WARNING: Operator has attempted to change the server seed after the commitment phase to alter the drops.\n")
        # 2. Independent Audit Instructions
        print("\n--- 2. INDEPENDENT AUDIT INSTRUCTIONS ---")
        print("You gacha pull may not be fair please do the following:")
        print("A ticket containing your audit script and transaction has been messaged to your account.")
        print("At the end of the ticket click the link to any of the following governing authorities")
        print("The governing authority will open a ticket and launch a relevant investigation for your ticket.")
        
                
        # Tamper original seed
        tampered_server_seed = server_seed + "altered_data" 
        
        # The system now attempts to verify the tampered seed against the original commitment hash
        verified = self.crypto.verify_commitment(tampered_server_seed, commitment)


if __name__ == "__main__":
    session = GameSession()
    # Run the session
    # 90 pulls to show the hard pity mechanic firing
    session.run_session(num_pulls=90)
   

