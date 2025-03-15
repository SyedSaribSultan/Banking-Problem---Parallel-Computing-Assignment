import time  # Import time module to simulate network delays
import threading  # Import threading to ensure thread-safe operations
from collections import defaultdict  # Import defaultdict for structured data handling

# ==============================================
# Distributed Banking System Using Vector Clocks
# ==============================================

class BankNode:
    def __init__(self, bank_id, total_banks):
        """
        Initializes a BankNode representing a bank in a distributed transaction system.
        Each bank maintains:
        - A unique bank_id to identify itself.
        - A vector clock to track transaction causality.
        - A hold-back queue for transactions that arrive out of order.
        - A list of processed transactions.
        - A threading lock to ensure safe concurrent access to shared resources.
        """
        self.bank_id = bank_id  # Unique identifier for the bank
        self.vector_clock = [0] * total_banks  # Initialize vector clock with zeroes
        self.hold_back_queue = []  # Buffer for out-of-order transactions
        self.processed_transactions = []  # Store successfully processed transactions
        self.lock = threading.Lock()  # Lock to prevent race conditions in multi-threaded execution

    def send_transaction(self, transaction, recipient_banks):
        """
        Sends a transaction from this bank to all recipient banks.
        - Increments the bank's own vector clock before sending.
        - Creates a transaction message with the updated vector clock.
        - Sends the transaction to all specified recipient banks.
        """
        with self.lock:  # Ensure thread safety
            self.vector_clock[self.bank_id] += 1  # Update local vector clock
            message = {
                'transaction': transaction,  # Transaction details
                'vector_clock': self.vector_clock.copy(),  # Attach a copy of the vector clock
                'sender': self.bank_id  # Identify the sender bank
            }

            print(f"Bank {self.bank_id} sends transaction: '{transaction}' with clock {self.vector_clock}")

            # Multicast transaction to recipient banks
            for bank in recipient_banks:
                bank.receive_transaction(message)

    def receive_transaction(self, message):
        """
        Handles incoming transactions.
        - Checks if the transaction can be processed immediately.
        - If not, stores it in the hold-back queue.
        """
        with self.lock:  # Ensure thread-safe operations
            sender = message['sender']  # Extract sender ID
            transaction = message['transaction']  # Extract transaction details
            received_vector = message['vector_clock']  # Extract sender's vector clock

            # Check if the transaction can be processed immediately
            if self.can_process(received_vector):
                self.process_transaction(message)
                self.check_hold_back_queue()  # Re-evaluate hold-back queue for possible deliveries
            else:
                print(f"Bank {self.bank_id} holding transaction from Bank {sender}: '{transaction}'")
                self.hold_back_queue.append(message)  # Store transaction for later

    def can_process(self, received_vector):
        """
        Determines if a received transaction can be processed immediately.
        - A transaction is processable if:
          1. The sender's event is the next expected (local[sender] + 1 == received_vector[sender]).
          2. All other banks' events are already acknowledged (local[i] >= received_vector[i]).
        """
        sender = received_vector.index(max(received_vector))  # Identify sender

        # Ensure sender's transaction is in sequence
        if self.vector_clock[sender] + 1 != received_vector[sender]:
            return False

        # Ensure all other processes are up to date
        for i in range(len(self.vector_clock)):
            if i != sender and self.vector_clock[i] < received_vector[i]:
                return False

        return True  # Transaction can be processed

    def process_transaction(self, message):
        """
        Processes a valid transaction.
        - Updates the vector clock to reflect the transaction.
        - Logs the processed transaction.
        """
        sender = message['sender']  # Identify sender bank
        transaction = message['transaction']  # Extract transaction details
        received_vector = message['vector_clock']  # Extract sender's vector clock

        self.vector_clock[sender] += 1  # Update vector clock for sender's event
        self.processed_transactions.append(transaction)  # Log processed transaction

        print(f"Bank {self.bank_id} processed transaction from Bank {sender}: '{transaction}'")

    def check_hold_back_queue(self):
        """
        Iterates over the hold-back queue to check if any pending transactions can now be processed.
        - Transactions are removed from the hold-back queue once processed.
        """
        delivered_now = []  # Store transactions that can now be processed

        for message in self.hold_back_queue:
            if self.can_process(message['vector_clock']):
                self.process_transaction(message)
                delivered_now.append(message)

        # Remove successfully processed transactions from the hold-back queue
        for message in delivered_now:
            self.hold_back_queue.remove(message)

# ==============================================
# Simulating the Banking Transactions
# ==============================================

def simulate_banking_transactions():
    """
    Simulates interbank transactions in a distributed system.
    - Creates three bank nodes.
    - Sends a deposit transaction from Bank 0.
    - Sends a withdrawal transaction from Bank 1 with a short delay.
    """
    total_banks = 3  # Define the number of banks in the system
    banks = [BankNode(i, total_banks) for i in range(total_banks)]  # Initialize bank nodes

    # Simulate transactions
    banks[0].send_transaction("Deposit $10,000", [banks[1], banks[2]])  # Bank 0 initiates a deposit
    time.sleep(0.5)  # Simulate network delay
    banks[1].send_transaction("Withdraw $10,000", [banks[0], banks[2]])  # Bank 1 initiates a withdrawal

# Run the simulation
simulate_banking_transactions()
