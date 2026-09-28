import time
from unittest.mock import patch
import main as main_module

def run_stress_test(num_players=10000):
    print(f"Starting stress test for {num_players} concurrent player pulls...")
    
    # Initialise the game session
    session = main_module.GameSession()
    
    # Start the high-resolution performance timer
    start_time = time.perf_counter()
    
    # Mock the input() function to  return a blank string
    # Simulates players relying on the server's secure random generation
    # Prevents the loop from pausing to ask for terminal input
    with patch('builtins.input', return_value=""):
        for _ in range(num_players):
            session.run_session(num_pulls=1)
            
    # Stop the timer
    end_time = time.perf_counter()
    
    # Calculated performance 
    total_time = end_time - start_time
    avg_time_per_pull = total_time / num_players
    pulls_per_second = num_players / total_time
    
    # RESULTS
    print("-" * 40)
    print("STRESS TEST RESULTS")
    print("-" * 40)
    print(f"Total time for {num_players} pulls: {total_time:.4f} seconds")
    print(f"Average time per pull:       {avg_time_per_pull:.6f} seconds")
    print(f"Estimated pulls per second:  {pulls_per_second:.2f} pulls/sec")
    print("-" * 40)

if __name__ == "__main__":
    run_stress_test()