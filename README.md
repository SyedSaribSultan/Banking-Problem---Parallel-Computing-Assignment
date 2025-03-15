Distributed Banking System Using Vector Clocks

Overview

This project simulates a distributed banking system where multiple banks exchange transactions using vector clocks to maintain causal consistency. It ensures that transactions are processed in the correct order across multiple banks in a distributed environment.

Features

Implements vector clocks to track and order transactions.

Supports causal ordering of transactions across different bank nodes.

Uses a hold-back queue to store out-of-order transactions until they can be safely processed.

Simulates message passing and transaction dependencies in a distributed banking system.

How It Works

Each bank node has a unique ID and a vector clock to track transaction order.

When a bank sends a transaction, it updates its vector clock and broadcasts the message to recipient banks.

A receiving bank checks if the transaction can be processed immediately:

If the transaction's dependencies are met, it is processed.

If dependencies are missing, the transaction is held back until it can be processed.

Once dependencies are resolved, transactions from the hold-back queue are processed in order.

Prerequisites

Python 3.x

Installation

Clone this repository or copy the script.

Ensure Python 3.x is installed on your system.

No additional dependencies are required.

Running the Simulation

Run the script using:

python banking_simulation.py

Expected Output

Example console output:

Bank 0 sends transaction: 'Deposit $10,000' with clock [1, 0, 0]
Bank 1 holding transaction from Bank 0: 'Deposit $10,000'
Bank 2 holding transaction from Bank 0: 'Deposit $10,000'
Bank 1 sends transaction: 'Withdraw $10,000' with clock [0, 1, 0]
Bank 0 holding transaction from Bank 1: 'Withdraw $10,000'
Bank 2 holding transaction from Bank 1: 'Withdraw $10,000'
Bank 0 processed transaction from Bank 1: 'Withdraw $10,000'
Bank 1 processed transaction from Bank 0: 'Deposit $10,000'
Bank 2 processed transaction from Bank 0: 'Deposit $10,000'
Bank 2 processed transaction from Bank 1: 'Withdraw $10,000'

Code Structure

BankNode Class

Maintains vector clocks.

Sends and receives transactions.

Manages the hold-back queue for out-of-order transactions.

simulate_banking_transactions() Function

Initializes multiple bank nodes.

Sends transactions between banks with simulated network delay.

Key Concepts Implemented

✔ Vector Clocks: Ensures that transactions are processed in causally correct order.
✔ Hold-Back Queue: Stores transactions until they can be safely executed.
✔ Concurrency & Synchronization: Uses locks to manage concurrent transactions safely.

Future Enhancements

Implement network communication instead of local function calls.

Introduce random delays and faults to simulate real-world conditions.

Extend to a multi-threaded network simulation using sockets.

License

This project is open-source. Feel free to modify and improve it.

Author

Syed Sarib Sultan
