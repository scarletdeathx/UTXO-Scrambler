# UTXO Scrambler

## Overview
The **UTXO Scrambler** is a Python-based utility designed to enhance transaction precision, randomness, and privacy within the Gridcoin ecosystem. While initially tailored for Gridcoin, it is adaptable to other UTXO-based cryptocurrencies that utilize 8-decimal outputs and customizable fees. This tool allows users to create transactions with randomized output structures while maintaining a designated allocation for a "real" receiver or change address.

By leveraging state randomness and controlled UTXO distribution, the tool supports blockchain throughput optimization, pseudonymity, and efficient staking practices for Proof of Stake (PoS) networks.

---

## Purpose and Motivation

1. **Randomness in Staking**:
   Gridcoin, like other PoS cryptocurrencies, benefits from randomness within transaction outputs. Randomized UTXO generation introduces entropy to the staking ecosystem, making patterns harder to predict and enhancing the security of staking processes.

2. **Throughput and Efficiency**:
   Random UTXO creation reduces computational bottlenecks and helps wallets reorganize inputs and outputs more effectively. The tool ensures that transactions utilize UTXOs efficiently, minimizing network congestion while enabling precise splitting of funds.

3. **Enhanced Privacy**:
   By incorporating randomly generated outputs into transactions, this tool obscures the direct correlation between inputs and outputs on the blockchain, boosting pseudonymity. While the change address acts as the "real" receiver, the randomized outputs act as padding to provide additional obfuscation.

4. **Flexibility for Other Blockchains**:
   Though designed with Gridcoin in mind, this tool's modularity allows it to adapt to other UTXO-based cryptocurrencies, provided they meet the basic structural requirements.

---

## Features

1. **Customizable Random Output Splitting**:
   - Generates randomized transaction outputs based on user-defined constraints (e.g., minimum and maximum amounts).
   - Precision down to 8 decimal places ensures accuracy and fairness in splitting.

2. **Change Address Allocation**:
   - Users can specify a percentage (`change_percent`) of the distributable amount to be sent to a "real" receiver (change address), while the remaining funds are distributed randomly.

3. **Configurable Parameters**:
   - Includes user-configurable fees, output constraints, randomization thresholds, and logging options via a simple configuration file.

4. **Transaction Integrity**:
   - Validates inputs and outputs to ensure compliance with the underlying cryptocurrency's requirements, preventing malformed transactions.

5. **Logging Support**:
   - Captures transaction details in an optional log file for debugging or auditing purposes.

---

## Configuration

The tool requires two primary configuration files: `scrambler.conf` and `inputs.json`.

### 1. `scrambler.conf`
This file defines the global settings for transaction creation:
```
fee = 0.001  # Typical Transaction fee in GRC
min_output = 0.01  # Minimum allowed output per address
max_output = 9.99999999  # Maximum allowed output per address
outputs_file = outputs.txt  # File containing recipient addresses
change_address = YOUR_CHANGE_ADDRESS  # The designated "real" receiver
change_percent = 70  # Percentage of leftover funds allocated to the change address
log_enabled = true  # Enable or disable logging
log_file = scrambler.log  # Path to the log file
```

### 2. `inputs.json`
This JSON file contains the UTXO inputs to be used in the transaction. The structure must follow the format:
```json
[
    {
        "txid": "0f8a353263151f36fac5a963484e1bf4c8cbf85eb140133bfe5e463bab94b538",
        "vout": 0,
        "amount": 69.33886696
    }
]
```

### 3. `outputs.txt`
A plain-text file listing the recipient addresses, one per line. Comments or blank lines are ignored.

---

## How It Works

### 1. Parsing Configuration and Inputs
The script reads parameters from `scrambler.conf` and parses the UTXOs from `inputs.json`. It validates all inputs to ensure compatibility with the transaction's requirements.

### 2. Random Distribution
Using cryptographic randomness, the script splits a user-defined portion of the total amount (`distributable = total_amount - fee`) among output addresses. It adheres to the constraints (`min_output` and `max_output`) to ensure validity.

### 3. Change Address Allocation
The remaining funds, defined by `change_percent`, are sent to the designated change address, ensuring precision and compliance with user specifications.

### 4. Output Validation and Logging
The script outputs the raw transaction in a Gridcoin-compatible format and optionally logs the transaction details for auditing purposes.

---

## Usage

1. **Run the Script**:
   Execute the script to generate a raw transaction:
   ```bash
   python3 scrambler.py
   ```
   The tool will output the raw transaction in JSON format and provide a CLI command for broadcasting it.

2. **Sign the Transaction**:
   Use the Gridcoin CLI to sign the transaction:
   ```bash
   gridcoin-cli signrawtransaction <unsigned_hex_string>
   ```

3. **Broadcast the Transaction**:
   Send the signed transaction to the blockchain:
   ```bash
   gridcoin-cli sendrawtransaction <signed_hex_string>
   ```

---

## Example Output
Sample CLI command generated by the script:
```bash
gridcoin-cli createrawtransaction '[{"txid": "0f8a353263151f36fac5a963484e1bf4c8cbf85eb140133bfe5e463bab94b538", "vout": 0}]' '{"SLiQUiD3hQRQLME7Pe2BCcFk2qqC8BhGUR": 4.19226223, "SLiQUiDBD3GeJfWW2LukKEhTg5UQe2oCeb": 2.51534805, "SDEAtHospu1SCUK2Mh8Pvdi27EBJFdQdeW": 6.93055669}'
```

---

## State Randomness and Blockchain Privacy

### Randomness and Proof of Stake
Randomness plays a crucial role in blockchain systems like Gridcoin, which rely on Proof of Stake (PoS) consensus mechanisms. By introducing pseudorandom outputs, this tool:
- Enhances validator anonymity, protecting participants from heuristic-based attacks.
- Promotes decentralization by evenly distributing outputs, supporting network health and fairness.
- Generates high-entropy UTXO sets, improving overall staking efficiency.

### Transaction Privacy
Incorporating randomized outputs obscures the relationship between inputs and outputs. By creating padding transactions, users can mitigate traceability while maintaining compliance with blockchain transparency requirements.

## Misc
This was designed to send liquidity to a staking wallet but send randomized inputs below Gridcon's staking eligibility threshold (10 GRC) but above its dust threshold (0.01) and to use 8 decimal points of precision. Please be sure to change the default configurations. I just uploaded my environment as an example.
---

## Contributions
Contributions are welcome! Whether you want to extend compatibility to other blockchains or propose new features feel free to submit a pull request or open an issue.

## Donations
I mostly made this for myself, but if you think this is useful you're than welcome to give me more excuses to use it:
Gridcoin: SDEAtHospu1SCUK2Mh8Pvdi27EBJFdQdeW
Bitcoin: bc1qdeath0shd56j3ws8cq6f7mtgwehc6chpshsknn
Litecoin: LaMiAXK6pq5BQ8TijgqCz47H6WRbKvoKFd
Monero: 84rHjDJ9Svx3eGoeHuY29cHX3k19x28qN1AN6do62uKSF7g9sn5ijUAcG7wYxvKXvVg2QTD5cTnwUi7sybQN9YZgSJxXgT8
---

## License
This project is licensed under the MIT License. See `LICENSE.md` for details.
```

---


