Project Title: How can cryptographic commitment schemes be designed and evaluated to improve the transparency and fairness of RNG-based loot systems in digital games?

Description: This project builds a cryptographic commitment scheme, that demonstrates a provably fair system can be mapped onto loot box mechanics. There are six files,
a cryptographic scheme, a gacha system, a main pull session, a test suite, a modelled stress test and a tamper demo


Note :
- Python 3.x 
- Pytest is required for running the test suite, to install pytest, run: pip install pytest



Instructions:
1. RUNNING THE MAIN SESSION
To run the  interactive gacha session, navigate to the project directory in your terminal and execute:

> python main.py

The session runs a defaulted 90 pulls. You will be prompted to provide an input to create your client seed. 
A script will  display the results of the 90-pull session and provide instructions on how to independently verify the cryptographic results.

2. RUNNING THE TEST SUITE
The test suite includes 13 unit and integration tests to ensure system functionality and integrity. 
To run the tests, execute:

> python -m pytest test_main.py -v

A verbose output showing all tests passing.

3. RUNNING THE STRESS TEST
To simulate 10,000 concurrent pulls and evaluate the system's performance, execute:

> python stress_test.py

The script outputs the total execution time, average time per pull, and pulls per second.


4. RUNNING THE TAMPER DEMO
The session simulates how the system responds in an altered server seed scenario, execute: 

> python tamper_demo.py

A session is run with the script flagging a verification warning.







Files: 

main.py: This file imports modules from crypto.py and gacha.py is where the main session is ran. The session runs at a defaulted 90 pulls, when running the session, it will ask for user input,
in order to create your client seed in line with the commitment scheme requirements. A script will be displayed showing all the results for a 90 pull session and instructions on how to independently verify results.

tamper_demo.py: This file runs the main session in the scenario that server-side tampering has occurred.

crypto.py: This file generates the cryptographic protocols for the commitment scheme.

gacha.py: This file creates the gacha system mechanics, the rarity tiers and pity mechanics are set up, and the hash-to-roll mechanics are set up.

test_main_.py: This is a test suite containing 13 unit tests, to ensure system functionality and integrity. Install pytest to use this.

stress_test_.py: This is a performance test that simulates 10,000 concurrent pulls.